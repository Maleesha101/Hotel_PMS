"""Tasks router – placeholder for later implementation."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/tasks")
async def list_tasks():
    return {"detail": "Tasks endpoint placeholder – to be implemented."}
