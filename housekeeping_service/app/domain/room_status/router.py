"""Room status router – stub implementation for initial import validation."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import HousekeepingTask
from app.schemas import TaskRead

router = APIRouter()

@router.post("/rooms/{room_id}/checkout", response_model=TaskRead)
async def simulate_checkout(room_id: str, room_type: str, db: AsyncSession = Depends(get_db)):
    """Triggered by checkout event: creates a CHECKOUT_CLEAN task."""
    task = HousekeepingTask(room_id=room_id, room_type=room_type, type="CHECKOUT_CLEAN", status="PENDING")
    db.add(task)
    await db.flush()
    return task
