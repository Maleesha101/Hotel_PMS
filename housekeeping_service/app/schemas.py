from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from pydantic import ConfigDict
from datetime import datetime

class InventoryItemCreate(BaseModel):
    name: str
    current_balance: int = 0

class InventoryItemRead(BaseModel):
    id: UUID
    name: str
    current_balance: int
    model_config = ConfigDict(from_attributes=True)

class RoomSupplyStandardCreate(BaseModel):
    room_type: str
    item_id: UUID
    quantity: int

class RoomSupplyStandardRead(BaseModel):
    id: UUID
    room_type: str
    item_id: UUID
    quantity: int 
    model_config = ConfigDict(from_attributes=True)

class TaskRead(BaseModel):
    id: UUID
    room_id: str
    room_type: str
    type: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    status: str

class TaskComplete(BaseModel):
    supplies_replaced: bool = True
    performed_by: Optional[str] = None

class DamageReportCreate(BaseModel):
    room_id: str
    task_id: Optional[UUID] = None
    item_description: str
    damage_type: str
    reported_by: str
    is_guest_chargeable: bool = False

class DamageReportRead(BaseModel):
    id: UUID
    room_id: str
    item_description: str
    damage_type: str
    is_guest_chargeable: bool
    status: str 
    model_config = ConfigDict(from_attributes=True)