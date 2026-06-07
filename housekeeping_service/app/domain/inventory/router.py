"""Inventory router – placeholder for future implementation."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/inventory")
async def list_inventory():
    return {"detail": "Inventory endpoint placeholder – to be implemented."}
