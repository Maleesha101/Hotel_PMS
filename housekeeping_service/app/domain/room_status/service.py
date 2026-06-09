"""Service layer for room status domain.

Provides high-level business logic and transaction management for room status changes,
specifically for use by background workers and internal messaging consumers.
"""

import logging
from typing import Optional
from app.database import AsyncSessionLocal
from app.domain.room_status import repository as rs_repo

logger = logging.getLogger(__name__)

async def patch_status(room_id: str, status: str, updated_by: str, note: Optional[str] = None):
    """Updates the status of a room. Used by messaging consumers.
    
    This function manages its own database transaction.
    """
    async with AsyncSessionLocal() as db:
        try:
            room = await rs_repo.update_status(
                db=db,
                room_id=room_id,
                new_status=status,
                updated_by=updated_by,
                status_note=note
            )
            await db.commit()
            return room
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to patch room status for room {room_id}: {str(e)}")
            raise