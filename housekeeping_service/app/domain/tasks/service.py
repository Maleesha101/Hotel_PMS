"""Service layer for housekeeping tasks."""

import logging
from app.domain.room_status import service as rs_service

logger = logging.getLogger(__name__)

async def create_task_from_checkout(room_id: str):
    """Processes a room checkout event.
    
    In the housekeeping service, a checkout necessitates a cleaning task.
    This function updates the room status to 'DIRTY' to notify staff.
    """
    try:
        # Update the room status to DIRTY using the existing room_status service
        await rs_service.patch_status(
            room_id=room_id,
            status="DIRTY",
            updated_by="SYSTEM_MESSAGING",
            note="Automated: Guest checked out, room requires cleaning."
        )
        logger.info(f"Checkout processed for room {room_id}. Status set to DIRTY.")
    except Exception as e:
        logger.error(f"Failed to process checkout for room {room_id}: {str(e)}")
        raise