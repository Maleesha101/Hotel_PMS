"""Supplies router – placeholder for future implementation."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import RoomSupplyStandard
from app.schemas import RoomSupplyStandardCreate, RoomSupplyStandardRead
from typing import List

router = APIRouter()

@router.post("/supplies", response_model=RoomSupplyStandardRead)
async def create_supply_standard(std_in: RoomSupplyStandardCreate, db: AsyncSession = Depends(get_db)):
    std = RoomSupplyStandard(**std_in.model_dump())
    db.add(std)
    await db.flush()
    return std

@router.get("/supplies", response_model=List[RoomSupplyStandardRead])
async def list_supplies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RoomSupplyStandard))
    return result.scalars().all()
