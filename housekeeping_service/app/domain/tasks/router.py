"""Tasks router – placeholder for later implementation."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import HousekeepingTask, RoomSupplyStandard, InventoryItem, InventoryTransaction
from app.schemas import TaskRead, TaskUpdate, TaskComplete
from typing import List
from uuid import UUID

router = APIRouter()

@router.get("/tasks", response_model=List[TaskRead])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HousekeepingTask))
    return result.scalars().all()

@router.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task_status(task_id: UUID, task_in: TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HousekeepingTask).where(HousekeepingTask.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = task_in.status
    return task

@router.post("/tasks/{task_id}/complete", response_model=TaskRead)
async def complete_task(task_id: UUID, complete_in: TaskComplete, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HousekeepingTask).where(HousekeepingTask.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = "COMPLETED"
    
    if complete_in.supplies_replaced:
        # Logic for inventory deduction based on Room Supply Standards
        std_result = await db.execute(select(RoomSupplyStandard).where(RoomSupplyStandard.room_type == task.room_type))
        standards = std_result.scalars().all()
        
        for std in standards:
            item_res = await db.execute(select(InventoryItem).where(InventoryItem.id == std.item_id))
            item = item_res.scalar_one()
            
            item.current_balance -= std.quantity
            
            # Record transaction for history and auditing
            tx = InventoryTransaction(
                item_id=item.id, transaction_type="ISSUE", quantity=std.quantity,
                balance_after=item.current_balance, room_id=task.room_id,
                task_id=task.id, performed_by=complete_in.performed_by
            )
            db.add(tx)
            
    return task
