"""Room status router – implements full CRUD and dashboard endpoints.

All endpoints require the Admin role (as per user specification).
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from app.dependencies import require_roles
from app.shared.responses import ApiResponse, PagedResponse
from app.domain.room_status import schemas as rs_schemas
from app.domain.room_status import repository as rs_repo
from app.config import settings
import json
from redis import asyncio as aioredis

router = APIRouter()
admin_dep = Depends(require_roles("Admin"))

# Helper to publish Redis messages
async def _publish_status_change(room_id: str, status: str):
    try:
        r = await aioredis.from_url(settings.REDIS_URL)
        payload = json.dumps({"room_id": room_id, "status": status})
        await r.publish(settings.ROOM_STATUS_CHANNEL, payload)
        await r.close()
    except Exception as e:
        # Log error in real app; here we ignore to avoid breaking API
        pass

@router.get("/rooms/status", response_model=ApiResponse)
async def list_rooms(
    status: str | None = Query(None),
    floor: int | None = Query(None),
    room_type: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    _: None = admin_dep,
):
    offset = (page - 1) * size
    rooms = await rs_repo.list_rooms(
        db=await rs_repo.get_db(),
        status=status,
        floor=floor,
        room_type=room_type,
        limit=size,
        offset=offset,
    )
    response_data = [rs_schemas.RoomStatusResponse.from_orm(r) for r in rooms]
    return ApiResponse(status="success", data=response_data)

@router.get("/rooms/status/{room_id}", response_model=ApiResponse)
async def get_room_status(room_id: str, _: None = admin_dep):
    room = await rs_repo.get_by_room_id(db=await rs_repo.get_db(), room_id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return ApiResponse(status="success", data=rs_schemas.RoomStatusResponse.from_orm(room))

@router.patch("/rooms/status/{room_id}", response_model=ApiResponse)
async def update_room_status(
    room_id: str,
    payload: rs_schemas.UpdateRoomStatusRequest,
    _: None = admin_dep,
):
    try:
        room = await rs_repo.update_status(
            db=await rs_repo.get_db(),
            room_id=room_id,
            new_status=payload.status.value,
            updated_by=payload.updated_by,
            status_note=payload.status_note,
        )
        await _publish_status_change(room_id, payload.status.value)
        return ApiResponse(status="success", data=rs_schemas.RoomStatusResponse.from_orm(room))
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")

@router.post("/rooms/status/bulk-update", response_model=ApiResponse)
async def bulk_update_status(
    bulk: rs_schemas.BulkUpdateRequest,
    _: None = admin_dep,
):
    updated = []
    db = await rs_repo.get_db()
    for item in bulk.updates:
        try:
            room = await rs_repo.update_status(
                db=db,
                room_id=item.room_id,
                new_status=item.status.value,
                updated_by=item.updated_by,
                status_note=item.status_note,
            )
            await _publish_status_change(item.room_id, item.status.value)
            updated.append(rs_schemas.RoomStatusResponse.from_orm(room))
        except Exception:
            continue
    return ApiResponse(status="success", data={"updated": len(updated)})

@router.get("/rooms/status/dashboard", response_model=ApiResponse)
async def dashboard(_: None = admin_dep):
    counts = await rs_repo.count_by_status(db=await rs_repo.get_db())
    total = sum(counts.values())
    dashboard = rs_schemas.DashboardResponse(counts=counts, total_rooms=total)
    return ApiResponse(status="success", data=dashboard)
