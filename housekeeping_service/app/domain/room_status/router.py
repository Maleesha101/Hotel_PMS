"""Room status router – stub implementation for initial import validation."""

from fastapi import APIRouter

router = APIRouter()

# Placeholder endpoints – will be fully implemented in later phases.
@router.get("/rooms/status")
async def list_rooms():
    return {"detail": "Endpoint placeholder – to be implemented."}
