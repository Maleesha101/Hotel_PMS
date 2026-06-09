"""Kafka consumer that runs as a FastAPI background task.

It subscribes to the three inbound topics and dispatches to the appropriate
service functions. Errors are retried up to three times; on permanent failure
the raw payload is sent to the dead‑letter topic ``hotel.housekeeping.dlq``.
"""

import json
import asyncio
from typing import Any

from aiokafka import AIOKafkaConsumer, ConsumerRecord
from app.config import settings
from app.dependencies import get_current_user  # ensures JWT deps are loaded
from app.domain.room_status.service import patch_status as room_patch_status
from app.domain.tasks.service import create_task_from_checkout

_consumer: AIOKafkaConsumer | None = None
_consumer_task: asyncio.Task | None = None
_MAX_RETRIES = 3
_DEAD_LETTER_TOPIC = "hotel.housekeeping.dlq"

async def _publish_dead_letter(payload: Any) -> None:
    from .producer import publish
    await publish({"payload": payload}, _DEAD_LETTER_TOPIC)

async def _process_message(msg: ConsumerRecord) -> None:
    payload = json.loads(msg.value.decode())
    if msg.topic == "hotel.booking.checkout":
        await create_task_from_checkout(room_id=payload.get("room_id"))
    elif msg.topic == "hotel.booking.checkin":
        await room_patch_status(
            room_id=payload["room_id"],
            new_status="OCCUPIED",
            updated_by="system",
            status_note="Guest checked in",
        )
    elif msg.topic == "hotel.maintenance.completed":
        if payload.get("room_ready_for_service"):
            await room_patch_status(
                room_id=payload["room_id"],
                new_status="CLEAN",
                updated_by="system",
                status_note="Maintenance completed",
            )
    else:
        await _publish_dead_letter({"topic": msg.topic, "payload": payload})

async def _consumer_loop() -> None:
    assert _consumer is not None
    async for msg in _consumer:
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                await _process_message(msg)
                break
            except Exception as exc:
                if attempt == _MAX_RETRIES:
                    await _publish_dead_letter({"topic": msg.topic, "payload": msg.value.decode()})
                await asyncio.sleep(0.5)

async def start_consumer() -> None:
    global _consumer, _consumer_task
    if _consumer is not None:
        return
    _consumer = AIOKafkaConsumer(
        "hotel.booking.checkout",
        "hotel.booking.checkin",
        "hotel.maintenance.completed",
        bootstrap_servers=settings.KAFKA_BOOTSTRAP,
        group_id=settings.KAFKA_CONSUMER_GROUP,
        enable_auto_commit=True,
        auto_offset_reset="earliest",
    )
    await _consumer.start()
    _consumer_task = asyncio.create_task(_consumer_loop())

async def stop_consumer() -> None:
    global _consumer, _consumer_task
    if _consumer:
        await _consumer.stop()
        _consumer = None
    if _consumer_task:
        _consumer_task.cancel()
        try:
            await _consumer_task
        except asyncio.CancelledError:
            pass
        _consumer_task = None
