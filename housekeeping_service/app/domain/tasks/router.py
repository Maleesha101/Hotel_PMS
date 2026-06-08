"""Tasks router – implements full CRUD and state transition endpoints.

All endpoints require the Admin role (as per user spec). Pagination defaults to size 20.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from typing import List

from app.dependencies import require_roles
from app.shared.responses import ApiResponse, PagedResponse
from app.domain.tasks import schemas as task_schemas
from app.domain.tasks import repository as task_repo
from app.domain.inventory import repository as inventory_repo
from app.config import settings
from app.messaging.producer import publish

router = APIRouter()
admin_dep = Depends(require_roles("Admin"))

# Helper to publish task completion events
async def _publish_task_completed(task_id: str, room_id: str, task_type: str):
    await publish({
        "task_id": task_id,
        "room_id": room_id,
        "task_type": task_type,
        "completed_at": datetime.utcnow().isoformat()
    }, settings.TASK_COMPLETED_TOPIC)

@router.post("/tasks", response_model=ApiResponse)
async def create_task(payload: task_schemas.TaskCreateRequest, _: None = admin_dep):
    task = await task_repo.create_task(db=await task_repo.get_db(), **payload.dict())
    return ApiResponse(status="success", data=task_schemas.TaskResponse.from_orm(task))

@router.get("/tasks", response_model=ApiResponse)
async def list_tasks(
    status: str | None = Query(None),
    room_id: str | None = Query(None),
    assigned_staff: str | None = Query(None),
    task_type: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    _: None = admin_dep,
):
    tasks = await task_repo.list_tasks(
        db=await task_repo.get_db(),
        status=status,
        room_id=room_id,
        assigned_staff=assigned_staff,
        task_type=task_type,
        limit=size,
        offset=(page - 1) * size,
    )
    data = [task_schemas.TaskResponse.from_orm(t) for t in tasks]
    return ApiResponse(status="success", data=data)

@router.get("/tasks/{task_id}", response_model=ApiResponse)
async def get_task(task_id: str, _: None = admin_dep):
    task = await task_repo.get_task(db=await task_repo.get_db(), task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return ApiResponse(status="success", data=task_schemas.TaskResponse.from_orm(task))

@router.patch("/tasks/{task_id}", response_model=ApiResponse)
async def update_task(task_id: str, payload: task_schemas.TaskUpdateRequest, _: None = admin_dep):
    task = await task_repo.update_task(db=await task_repo.get_db(), task_id=task_id, **payload.dict(exclude_unset=True))
    return ApiResponse(status="success", data=task_schemas.TaskResponse.from_orm(task))

@router.post("/tasks/{task_id}/start", response_model=ApiResponse)
async def start_task(task_id: str, _: None = admin_dep):
    task = await task_repo.get_task(db=await task_repo.get_db(), task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != "PENDING":
        raise HTTPException(status_code=400, detail="Task cannot be started")
    updated = await task_repo.update_task(
        db=await task_repo.get_db(),
        task_id=task_id,
        status="IN_PROGRESS",
        started_at=datetime.utcnow(),
    )
    return ApiResponse(status="success", data=task_schemas.TaskResponse.from_orm(updated))

@router.post("/tasks/{task_id}/complete", response_model=ApiResponse)
async def complete_task(task_id: str, _: None = admin_dep):
    task = await task_repo.get_task(db=await task_repo.get_db(), task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != "IN_PROGRESS":
        raise HTTPException(status_code=400, detail="Task not in progress")
    # Simplified inventory deduction: if supplies_replaced provided, decrement those items
    if task.supplies_replaced:
        for sup in task.supplies_replaced:
            await inventory_repo.update_item(
                db=await inventory_repo.get_db(),
                item_id=sup["item_id"],
                available_qty=InventoryItemModel.available_qty - sup.get("qty", 0),
            )
    updated = await task_repo.update_task(
        db=await task_repo.get_db(),
        task_id=task_id,
        status="COMPLETED",
        completed_at=datetime.utcnow(),
    )
    await _publish_task_completed(task_id, task.room_id, task.task_type)
    return ApiResponse(status="success", data=task_schemas.TaskResponse.from_orm(updated))

@router.post("/tasks/{task_id}/reject", response_model=ApiResponse)
async def reject_task(task_id: str, reason: str | None = Query(None), _: None = admin_dep):
    task = await task_repo.get_task(db=await task_repo.get_db(), task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = await task_repo.update_task(
        db=await task_repo.get_db(),
        task_id=task_id,
        status="REJECTED",
        cleaning_notes=reason,
    )
    return ApiResponse(status="success", data=task_schemas.TaskResponse.from_orm(updated))

@router.get("/tasks/my-tasks", response_model=ApiResponse)
async def my_tasks(current_user=Depends(require_roles("Admin"))):
    # current_user is TokenPayload; filter by sub
    tasks = await task_repo.list_tasks(
        db=await task_repo.get_db(),
        assigned_staff=current_user.sub,
        limit=100,
        offset=0,
    )
    data = [task_schemas.TaskResponse.from_orm(t) for t in tasks]
    return ApiResponse(status="success", data=data)
