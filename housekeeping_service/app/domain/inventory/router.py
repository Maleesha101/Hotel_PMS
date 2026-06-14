"""Inventory router – implements full CRUD, transaction handling, low‑stock and summary endpoints.

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import InventoryItem
from app.schemas import InventoryItemCreate, InventoryItemRead
from typing import List

router = APIRouter()
admin_dep = Depends(require_roles("Admin"))

@router.post("/inventory", response_model=ApiResponse)
async def create_inventory_item(payload: inv_schemas.CreateInventoryItemRequest, db=Depends(get_db), _: None = admin_dep):
    item = await inv_repo.create_item(db=db, **payload.dict())
    return ApiResponse(status="success", data=inv_schemas.InventoryItemResponse.from_orm(item))

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
    data = [inv_schemas.InventoryItemResponse.from_orm(i) for i in items]
    return ApiResponse(status="success", data=data)

@router.get("/inventory/{item_id}", response_model=ApiResponse)
async def get_inventory_item(item_id: str, db=Depends(get_db), _: None = admin_dep):
    item = await inv_repo.get_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ApiResponse(status="success", data=inv_schemas.InventoryItemResponse.from_orm(item))

@router.patch("/inventory/{item_id}", response_model=ApiResponse)
async def update_inventory_item(item_id: str, payload: inv_schemas.UpdateInventoryItemRequest, db=Depends(get_db), _: None = admin_dep):
    item = await inv_repo.update_item(db=db, item_id=item_id, **payload.dict(exclude_unset=True))
    return ApiResponse(status="success", data=inv_schemas.InventoryItemResponse.from_orm(item))

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
    return ApiResponse(status="success", data=inv_schemas.InventoryTransactionResponse.from_orm(tx))

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
    return ApiResponse(status="success", data=inv_schemas.InventoryTransactionResponse.from_orm(tx))

@router.get("/inventory/{item_id}/transactions", response_model=ApiResponse)
async def get_item_transactions(
    item_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db=Depends(get_db),
    _: None = admin_dep,
):
    txs = await inv_repo.list_transactions(db=db, item_id=item_id, page=page, size=size)
    data = [inv_schemas.InventoryTransactionResponse.from_orm(t) for t in txs]
    return ApiResponse(status="success", data=data)

@router.get("/inventory/low-stock", response_model=ApiResponse)
async def low_stock_items(db=Depends(get_db), _: None = admin_dep):
    items = await inv_repo.low_stock_items(db=db)
    data = [inv_schemas.InventoryItemResponse.from_orm(i) for i in items]
    return ApiResponse(status="success", data=data)

@router.post("/inventory", response_model=InventoryItemRead)
async def create_inventory_item(item_in: InventoryItemCreate, db: AsyncSession = Depends(get_db)):
    item = InventoryItem(**item_in.model_dump())
    db.add(item)
    await db.flush()
    return item

@router.get("/inventory", response_model=List[InventoryItemRead])
async def list_inventory(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InventoryItem))
    return result.scalars().all()
