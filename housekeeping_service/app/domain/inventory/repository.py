"""Repository layer for inventory domain.

Provides async CRUD helpers for inventory items and transactions.
"""

from typing import List, Optional, Dict
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.inventory.model import InventoryItemModel
from app.domain.inventory.transaction_model import InventoryTransactionModel
from app.shared.enums import TransactionType, InventoryCategory

# -------------------- Inventory Item Helpers --------------------

async def create_item(db: AsyncSession, **kwargs) -> InventoryItemModel:
    item = InventoryItemModel(**kwargs)
    db.add(item)
    await db.flush()
    return item

async def get_item(db: AsyncSession, item_id: str) -> Optional[InventoryItemModel]:
    result = await db.execute(select(InventoryItemModel).where(InventoryItemModel.id == item_id))
    return result.scalars().first()

async def list_items(
    db: AsyncSession,
    *,
    category: Optional[InventoryCategory] = None,
    low_stock: Optional[bool] = None,
    supplier: Optional[str] = None,
    page: int = 1,
    size: int = 20,
) -> List[InventoryItemModel]:
    stmt = select(InventoryItemModel)
    if category:
        stmt = stmt.where(InventoryItemModel.category == category)
    if supplier:
        stmt = stmt.where(InventoryItemModel.supplier_name == supplier)
    if low_stock:
        stmt = stmt.where(InventoryItemModel.available_qty <= InventoryItemModel.min_stock_level)
    stmt = stmt.offset((page - 1) * size).limit(size)
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_item(db: AsyncSession, item_id: str, **fields) -> InventoryItemModel:
    await db.execute(update(InventoryItemModel).where(InventoryItemModel.id == item_id).values(**fields))
    await db.flush()
    return await get_item(db, item_id)

# -------------------- Inventory Transaction Helpers --------------------

async def create_transaction(
    db: AsyncSession,
    *,
    item_id: str,
    transaction_type: TransactionType,
    quantity: int,
    room_id: Optional[str] = None,
    task_id: Optional[str] = None,
    performed_by: Optional[str] = None,
    notes: Optional[str] = None,
) -> InventoryTransactionModel:
    # Fetch current balance
    item = await get_item(db, item_id)
    if not item:
        raise ValueError("Inventory item not found")
    # Compute new balance based on type
    if transaction_type == TransactionType.ADD:
        new_balance = item.available_qty + quantity
    else:
        # ISSUE or others decrease stock
        new_balance = item.available_qty - quantity
        if new_balance < 0:
            raise ValueError("Insufficient stock for transaction")
    # Update item quantity
    await db.execute(update(InventoryItemModel).where(InventoryItemModel.id == item_id).values(available_qty=new_balance))

    tx = InventoryTransactionModel(
        item_id=item_id,
        transaction_type=transaction_type.value,
        quantity=quantity,
        balance_after=new_balance,
        room_id=room_id,
        task_id=task_id,
        performed_by=performed_by,
        notes=notes,
    )
    db.add(tx)
    await db.flush()
    return tx

async def list_transactions(
    db: AsyncSession, *, item_id: str, page: int = 1, size: int = 20
) -> List[InventoryTransactionModel]:
    stmt = (
        select(InventoryTransactionModel)
        .where(InventoryTransactionModel.item_id == item_id)
        .order_by(InventoryTransactionModel.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def low_stock_items(db: AsyncSession) -> List[InventoryItemModel]:
    stmt = select(InventoryItemModel).where(InventoryItemModel.available_qty <= InventoryItemModel.min_stock_level)
    result = await db.execute(stmt)
    return result.scalars().all()

async def summary_by_category(db: AsyncSession) -> List[Dict]:
    stmt = (
        select(
            InventoryItemModel.category,
            func.count().label("total_items"),
            func.sum(InventoryItemModel.available_qty * InventoryItemModel.unit_cost).label("total_value"),
            func.sum(
                func.case(
                    [(InventoryItemModel.available_qty <= InventoryItemModel.min_stock_level, 1)], else_=0
                )
            ).label("low_stock_count"),
        )
        .group_by(InventoryItemModel.category)
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [
        {
            "category": r[0],
            "total_items": r[1],
            "total_value": float(r[2] or 0),
            "low_stock_count": r[3] or 0,
        }
        for r in rows
    ]
