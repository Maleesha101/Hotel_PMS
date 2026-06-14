"""Supplies router – implements CRUD for room supply standards.

All endpoints require the Admin role.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from app.dependencies import require_roles
from app.shared.responses import ApiResponse, PagedResponse
from app.domain.supplies import schemas as sup_schemas
from app.domain.supplies import repository as sup_repo
from app.database import get_db

router = APIRouter()
admin_dep = Depends(require_roles("Admin"))

@router.get("/supplies", response_model=ApiResponse)
async def list_supplies(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    _: None = admin_dep,
    db=Depends(get_db),
):
    supplies = await sup_repo.list_supplies(db, limit=size, offset=(page - 1) * size)
    data = [sup_schemas.SupplyStandardResponse.from_orm(s) for s in supplies]
    return ApiResponse(status="success", data=data)

@router.get("/supplies/{room_type}", response_model=ApiResponse)
async def get_supplies_by_room_type(
    room_type: str,
    _: None = admin_dep,
    db=Depends(get_db),
):
    supplies = await sup_repo.get_by_room_type(db, room_type)
    data = [sup_schemas.SupplyStandardResponse.from_orm(s) for s in supplies]
    return ApiResponse(status="success", data=data)

@router.post("/supplies", response_model=ApiResponse)
async def create_supply(payload: sup_schemas.CreateSupplyStandardRequest, _: None = admin_dep, db=Depends(get_db)):
    standard = await sup_repo.create_standard(db, **payload.dict())
    return ApiResponse(status="success", data=sup_schemas.SupplyStandardResponse.from_orm(standard))

@router.patch("/supplies/{standard_id}", response_model=ApiResponse)
async def update_supply(standard_id: str, payload: sup_schemas.UpdateSupplyStandardRequest, _: None = admin_dep, db=Depends(get_db)):
    standard = await sup_repo.update_standard(db, standard_id, **payload.dict(exclude_unset=True))
    return ApiResponse(status="success", data=sup_schemas.SupplyStandardResponse.from_orm(standard))

@router.delete("/supplies/{standard_id}", response_model=ApiResponse)
async def deactivate_supply(standard_id: str, _: None = admin_dep, db=Depends(get_db)):
    await sup_repo.deactivate_standard(db, standard_id)
    return ApiResponse(status="success", message="Supply standard deactivated")
