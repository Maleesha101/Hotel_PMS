"""Damage router – placeholder for future implementation."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/damage")
async def list_damage_reports():
    return {"detail": "Damage endpoint placeholder – to be implemented."}
