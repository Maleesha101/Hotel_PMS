"""Kafka producer utility for the housekeeping service.

The producer is created lazily on first use and started during the FastAPI
lifespan. All events are serialized as JSON strings.
"""

import json
from typing import Any

from aiokafka import AIOKafkaProducer
from app.config import settings

_producer: AIOKafkaProducer | None = None

async def init_producer() -> None:
    """Initialise the global ``AIOKafkaProducer`` instance.

    This should be called from the FastAPI lifespan start‑up phase.
    """
    global _producer
    if _producer is None:
        _producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP)
        await _producer.start()

async def close_producer() -> None:
    """Gracefully shut down the global producer if it exists."""
    global _producer
    if _producer is not None:
        await _producer.stop()
        _producer = None

async def publish(event: Any, topic: str) -> None:
    """Publish a Pydantic ``BaseModel`` (or any JSON‑serialisable object) to *topic*.

    The payload is encoded as UTF‑8 JSON. Raises ``RuntimeError`` if the
    producer has not been initialised.
    """
    if _producer is None:
        raise RuntimeError("Kafka producer has not been initialised")
    # ``event`` may be a Pydantic model; ``json.dumps`` will call ``dict`` on it.
    payload = json.dumps(event.dict() if hasattr(event, "dict") else event).encode()
    await _producer.send_and_wait(topic, payload)
