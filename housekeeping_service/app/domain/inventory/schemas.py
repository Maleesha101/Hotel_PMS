"""Pydantic schemas for the inventory domain.

These schemas are used by the FastAPI endpoints to validate request bodies
and shape responses.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel, Field, ConfigDict
from app.shared.enums import InventoryCategory, TransactionType

class InventoryItemResponse(BaseModel):
    id: str
    name: str
    category: InventoryCategory
    sku: Optional[str]
    available_qty: int
    min_stock_level: int
    unit: Optional[str]
    unit_cost: Optional[float]
    supplier_name: Optional[str]
    supplier_contact: Optional[str]
    location: Optional[str]
    is_active: bool
    last_restocked_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CreateInventoryItemRequest(BaseModel):
    name: str = Field(..., description="Item name")
    category: InventoryCategory = Field(..., description="Category of the inventory item")
    sku: Optional[str] = None
    available_qty: int = Field(0, ge=0)
    min_stock_level: int = Field(5, ge=0)
    unit: Optional[str] = None
    unit_cost: Optional[float] = Field(None, ge=0)
    supplier_name: Optional[str] = None
    supplier_contact: Optional[str] = None
    location: Optional[str] = None
    is_active: bool = True

class UpdateInventoryItemRequest(BaseModel):
    name: Optional[str] = None
    category: Optional[InventoryCategory] = None
    sku: Optional[str] = None
    available_qty: Optional[int] = Field(None, ge=0)
    min_stock_level: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = None
    unit_cost: Optional[float] = Field(None, ge=0)
    supplier_name: Optional[str] = None
    supplier_contact: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None

class TransactionRequest(BaseModel):
    quantity: int = Field(..., gt=0)
    performed_by: str = Field(..., description="User performing the transaction")
    notes: Optional[str] = None
    room_id: Optional[str] = None
    task_id: Optional[str] = None

class InventoryTransactionResponse(BaseModel):
    id: str
    item_id: str
    transaction_type: TransactionType
    quantity: int
    balance_after: int
    room_id: Optional[str]
    task_id: Optional[str]
    performed_by: Optional[str]
    notes: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class InventorySummaryResponse(BaseModel):
    category: str
    total_items: int
    total_value: float
    low_stock_count: int
