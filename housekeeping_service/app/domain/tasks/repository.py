"""Repository layer for housekeeping tasks.

Provides async CRUD and filter helpers.
"""

from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.tasks.model import HousekeepingTaskModel

async def create_task(db: AsyncSession, **kwargs) -> HousekeepingTaskModel:
    task = HousekeepingTaskModel(**kwargs)
    db.add(task)
    await db.flush()
    return task

async def get_task(db: AsyncSession, task_id: str) -> Optional[HousekeepingTaskModel]:
    result = await db.execute(select(HousekeepingTaskModel).where(HousekeepingTaskModel.id == task_id))
    return result.scalars().first()

async def list_tasks(
    db: AsyncSession,
    *,
    status: Optional[str] = None,
    room_id: Optional[str] = None,
    assigned_staff: Optional[str] = None,
    task_type: Optional[str] = None,
    date: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[HousekeepingTaskModel]:
    stmt = select(HousekeepingTaskModel)
    if status:
        stmt = stmt.where(HousekeepingTaskModel.status == status)
    if room_id:
        stmt = stmt.where(HousekeepingTaskModel.room_id == room_id)
    if assigned_staff:
        stmt = stmt.where(HousekeepingTaskModel.assigned_staff == assigned_staff)
    if task_type:
        stmt = stmt.where(HousekeepingTaskModel.task_type == task_type)
    # date filter can be expanded as needed
    stmt = stmt.limit(limit).offset(offset)
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_task(db: AsyncSession, task_id: str, **fields) -> HousekeepingTaskModel:
    await db.execute(
        update(HousekeepingTaskModel)
        .where(HousekeepingTaskModel.id == task_id)
        .values(**fields)
    )
    await db.flush()
    return await get_task(db, task_id)

async def delete_task(db: AsyncSession, task_id: str) -> None:
    await db.execute(delete(HousekeepingTaskModel).where(HousekeepingTaskModel.id == task_id))
    await db.flush()
