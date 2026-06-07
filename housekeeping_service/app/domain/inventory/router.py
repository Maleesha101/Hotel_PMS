"""Inventory router – placeholder for future implementation."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import InventoryItem
from app.schemas import InventoryItemCreate, InventoryItemRead
from typing import List

router = APIRouter()

@router.post("/inventory", response_model=InventoryItemRead)
async def create_inventory_item(item_in: InventoryItemCreate, db: AsyncSession = Depends(get_db)):
    item = InventoryItem(**item_in.model_dump())
    db.add(item)
    await db.flush()
    return item

@router.get("/inventory", response_model=List[InventoryItemRead])
async def list_inventory(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InventoryItem))
    return result.scalars().all()
