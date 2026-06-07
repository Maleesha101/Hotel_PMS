"""Supplies router – placeholder for future implementation."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/supplies")
async def list_supplies():
    return {"detail": "Supplies endpoint placeholder – to be implemented."}
