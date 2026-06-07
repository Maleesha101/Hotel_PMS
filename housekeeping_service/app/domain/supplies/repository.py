"""Repository layer for room supply standards.

Provides async CRUD helpers for the ``room_supply_standards`` table.
"""

from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.supplies.model import RoomSupplyStandardModel

async def create_standard(db: AsyncSession, **kwargs) -> RoomSupplyStandardModel:
    standard = RoomSupplyStandardModel(**kwargs)
    db.add(standard)
    await db.flush()
    return standard

async def get_by_id(db: AsyncSession, standard_id: str) -> Optional[RoomSupplyStandardModel]:
    result = await db.execute(select(RoomSupplyStandardModel).where(RoomSupplyStandardModel.id == standard_id))
    return result.scalars().first()

async def get_by_room_type(db: AsyncSession, room_type: str) -> List[RoomSupplyStandardModel]:n    result = await db.execute(select(RoomSupplyStandardModel).where(RoomSupplyStandardModel.room_type == room_type, RoomSupplyStandardModel.is_active == True))
    return result.scalars().all()

async def update_standard(db: AsyncSession, standard_id: str, **fields) -> RoomSupplyStandardModel:
    await db.execute(update(RoomSupplyStandardModel).where(RoomSupplyStandardModel.id == standard_id).values(**fields))
    await db.flush()
    return await get_by_id(db, standard_id)

async def deactivate_standard(db: AsyncSession, standard_id: str) -> None:
    await db.execute(update(RoomSupplyStandardModel).where(RoomSupplyStandardModel.id == standard_id).values(is_active=False))
    await db.flush()

async def delete_standard(db: AsyncSession, standard_id: str) -> None:
    await db.execute(delete(RoomSupplyStandardModel).where(RoomSupplyStandardModel.id == standard_id))
    await db.flush()
