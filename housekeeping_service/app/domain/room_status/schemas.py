"""Pydantic schemas for the room_status domain."""

from __future__ import annotations

from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.shared.enums import RoomStatus

class RoomStatusResponse(BaseModel):
    id: str = Field(..., description="UUID of the room status record")
    room_id: str = Field(..., description="Shared identifier with Reservation Service")
    room_number: str = Field(..., description="Human‑readable room number")
    floor: Optional[int] = Field(None, description="Floor number")
    room_type: Optional[str] = Field(None, description="Room type (SINGLE, DOUBLE, etc.)")
    status: RoomStatus = Field(..., description="Current live status of the room")
    previous_status: Optional[RoomStatus] = Field(None, description="Previous status before the change")
    updated_by: Optional[str] = Field(None, description="Staff user ID performing last update")
    status_note: Optional[str] = Field(None, description="Optional note explaining the status change")
    last_checkout: Optional[datetime] = Field(None, description="Timestamp of last checkout")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Record last update timestamp")

    model_config = ConfigDict(from_attributes=True)

class UpdateRoomStatusRequest(BaseModel):
    status: RoomStatus = Field(..., description="New room status", example="CLEAN")
    updated_by: str = Field(..., description="Staff user ID making the update", example="staff-001")
    status_note: Optional[str] = Field(None, description="Optional note for the status change", example="Deep clean completed")

class BulkUpdateItem(BaseModel):
    room_id: str = Field(..., description="Room identifier")
    status: RoomStatus = Field(..., description="Desired status")
    updated_by: str = Field(..., description="Staff performing the update")
    status_note: Optional[str] = Field(None, description="Optional note")

class BulkUpdateRequest(BaseModel):
    updates: List[BulkUpdateItem] = Field(..., description="List of room status updates")

class DashboardResponse(BaseModel):
    counts: Dict[RoomStatus, int] = Field(..., description="Mapping of status to number of rooms")
    total_rooms: int = Field(..., description="Total number of rooms tracked")
