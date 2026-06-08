"""Pydantic schemas for the supplies domain.

These define request and response models for room supply standards.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.shared.enums import RoomStatus

class SupplyStandardResponse(BaseModel):
    id: str
    room_type: str
    item_name: str
    category: str
    quantity: int
    unit: Optional[str]
    is_active: bool
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CreateSupplyStandardRequest(BaseModel):
    room_type: str = Field(..., description="Room type the supply applies to")
    item_name: str = Field(..., description="Name of the supply item")
    category: str = Field(..., description="Category of the supply")
    quantity: int = Field(..., description="Default quantity for the room type")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    notes: Optional[str] = Field(None, description="Additional notes")

class UpdateSupplyStandardRequest(BaseModel):
    quantity: Optional[int] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None
