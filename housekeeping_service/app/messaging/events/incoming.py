"""Pydantic models for events consumed from Kafka.

These correspond exactly to the contracts described in the specification.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class BookingCheckedOutEvent(BaseModel):
    booking_ref: str = Field(..., description="Booking reference")
    room_id: str = Field(..., description="Room identifier shared with reservation service")
    room_number: str = Field(..., description="Human‑readable room number")
    guest_name: str = Field(..., description="Guest full name")
    checkout_time: datetime = Field(..., description="Timestamp of checkout")
    has_complaint: bool = Field(..., description="Whether a complaint was filed")
    complaint_id: Optional[str] = Field(None, description="Optional complaint identifier")

class BookingCheckedInEvent(BaseModel):
    booking_ref: str = Field(..., description="Booking reference")
    room_id: str = Field(..., description="Room identifier")
    room_number: str = Field(..., description="Room number")
    guest_name: str = Field(..., description="Guest name")
    checkin_time: datetime = Field(..., description="Timestamp of check‑in")

class MaintenanceCompletedEvent(BaseModel):
    request_id: str = Field(..., description="Maintenance request identifier")
    room_id: str = Field(..., description="Room identifier")
    room_ready_for_service: bool = Field(..., description="Flag indicating room is ready")
    completed_at: datetime = Field(..., description="When maintenance was finished")
