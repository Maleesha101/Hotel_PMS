"""Repository layer for room status domain.

Provides async CRUD operations using SQLAlchemy session.
"""

from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.room_status.model import RoomStatusModel

async def get_by_room_id(db: AsyncSession, room_id: str) -> Optional[RoomStatusModel]:
    result = await db.execute(select(RoomStatusModel).where(RoomStatusModel.room_id == room_id))
    return result.scalars().first()

async def list_rooms(db: AsyncSession, *, status: Optional[str] = None, floor: Optional[int] = None, room_type: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[RoomStatusModel]:
    stmt = select(RoomStatusModel)
    if status:
        stmt = stmt.where(RoomStatusModel.status == status)
    if floor is not None:
        stmt = stmt.where(RoomStatusModel.floor == floor)
    if room_type:
        stmt = stmt.where(RoomStatusModel.room_type == room_type)
    stmt = stmt.limit(limit).offset(offset)
    result = await db.execute(stmt)
    return result.scalars().all()

async def count_by_status(db: AsyncSession) -> dict:
    stmt = select(RoomStatusModel.status, func.count()).group_by(RoomStatusModel.status)
    result = await db.execute(stmt)
    return {status: count for status, count in result.all()}

async def create_room_status(db: AsyncSession, *, room_id: str, room_number: str, floor: Optional[int] = None, room_type: Optional[str] = None, status: str = "VACANT", updated_by: Optional[str] = None, status_note: Optional[str] = None) -> RoomStatusModel:
    obj = RoomStatusModel(
        room_id=room_id,
        room_number=room_number,
        floor=floor,
        room_type=room_type,
        status=status,
        updated_by=updated_by,
        status_note=status_note,
    )
    db.add(obj)
    await db.flush()
    return obj

async def update_status(
    db: AsyncSession,
    *,
    room_id: str,
    new_status: str,
    updated_by: str,
    status_note: Optional[str] = None,
) -> RoomStatusModel:
    room = await get_by_room_id(db, room_id)
    if not room:
        raise ValueError("Room not found")
    room.previous_status = room.status
    room.status = new_status
    room.updated_by = updated_by
    room.status_note = status_note
    await db.flush()
    return room
