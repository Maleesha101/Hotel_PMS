"""Inventory router – implements full CRUD, transaction handling, low‑stock and summary endpoints.

All endpoints require the Admin role. Pagination defaults to page size 20.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from app.dependencies import require_roles
from app.shared.responses import ApiResponse
from app.database import get_db
from app.config import settings
from app.messaging.producer import publish

from app.shared.enums import TransactionType
from app.domain.inventory import schemas as inv_schemas
from app.domain.inventory import repository as inv_repo
from app.domain.inventory.model import InventoryItemModel

router = APIRouter()
admin_dep = Depends(require_roles("Admin"))

@router.post("/inventory", response_model=ApiResponse)
async def create_inventory_item(payload: inv_schemas.CreateInventoryItemRequest, db=Depends(get_db), _: None = admin_dep):
    item = await inv_repo.create_item(db=db, **payload.model_dump())
    return ApiResponse(status="success", data=inv_schemas.InventoryItemResponse.model_validate(item))

@router.get("/inventory", response_model=ApiResponse)
async def list_inventory(
    category: str | None = Query(None),
    low_stock: bool = Query(False),
    supplier: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db=Depends(get_db),
    _: None = admin_dep,
):
    items = await inv_repo.list_items(
        db=db,
        category=category,
        low_stock=low_stock,
        supplier=supplier,
        page=page,
        size=size,
    )
    data = [inv_schemas.InventoryItemResponse.model_validate(i) for i in items]
    return ApiResponse(status="success", data=data)

@router.get("/inventory/{item_id}", response_model=ApiResponse)
async def get_inventory_item(item_id: str, db=Depends(get_db), _: None = admin_dep):
    item = await inv_repo.get_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ApiResponse(status="success", data=inv_schemas.InventoryItemResponse.model_validate(item))

@router.patch("/inventory/{item_id}", response_model=ApiResponse)
async def update_inventory_item(item_id: str, payload: inv_schemas.UpdateInventoryItemRequest, db=Depends(get_db), _: None = admin_dep):
    item = await inv_repo.update_item(db=db, item_id=item_id, **payload.model_dump(exclude_unset=True))
    return ApiResponse(status="success", data=inv_schemas.InventoryItemResponse.model_validate(item))

@router.post("/inventory/{item_id}/restock", response_model=ApiResponse)
async def restock_item(item_id: str, payload: inv_schemas.TransactionRequest, db=Depends(get_db), _: None = admin_dep):
    tx = await inv_repo.create_transaction(
        db=db,
        item_id=item_id,
        transaction_type=TransactionType.ADD,
        quantity=payload.quantity,
        performed_by=payload.performed_by,
        notes=payload.notes,
        room_id=payload.room_id,
        task_id=payload.task_id,
    )
    await publish(tx.__dict__, settings.INVENTORY_TX_TOPIC)
    return ApiResponse(status="success", data=inv_schemas.InventoryTransactionResponse.model_validate(tx))

@router.post("/inventory/{item_id}/issue", response_model=ApiResponse)
async def issue_item(item_id: str, payload: inv_schemas.TransactionRequest, db=Depends(get_db), _: None = admin_dep):
    tx = await inv_repo.create_transaction(
        db=db,
        item_id=item_id,
        transaction_type=TransactionType.ISSUE,
        quantity=payload.quantity,
        performed_by=payload.performed_by,
        notes=payload.notes,
        room_id=payload.room_id,
        task_id=payload.task_id,
    )
    await publish(tx.__dict__, settings.INVENTORY_TX_TOPIC)
    return ApiResponse(status="success", data=inv_schemas.InventoryTransactionResponse.model_validate(tx))

@router.get("/inventory/{item_id}/transactions", response_model=ApiResponse)
async def get_item_transactions(
    item_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db=Depends(get_db),
    _: None = admin_dep,
):
    txs = await inv_repo.list_transactions(db=db, item_id=item_id, page=page, size=size)
    data = [inv_schemas.InventoryTransactionResponse.model_validate(t) for t in txs]
    return ApiResponse(status="success", data=data)

@router.get("/inventory/low-stock", response_model=ApiResponse)
async def low_stock_items(db=Depends(get_db), _: None = admin_dep):
    items = await inv_repo.low_stock_items(db=db)
    data = [inv_schemas.InventoryItemResponse.model_validate(i) for i in items]
    return ApiResponse(status="success", data=data)

@router.get("/inventory/summary", response_model=ApiResponse)
async def inventory_summary(db=Depends(get_db), _: None = admin_dep):
    summary = await inv_repo.summary_by_category(db=db)
    return ApiResponse(status="success", data=summary)
