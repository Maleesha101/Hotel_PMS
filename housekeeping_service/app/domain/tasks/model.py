"""SQLAlchemy model for housekeeping_tasks table."""

import uuid
from sqlalchemy import Column, String, Text, DateTime, Enum, JSON, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from app.models import Base
from app.shared.enums import TaskStatus, TaskType

class HousekeepingTaskModel(Base):
    __tablename__ = "housekeeping_tasks"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = Column(String(50), nullable=False)
    room_number = Column(String(20), nullable=False)
    booking_ref = Column(String(100))
    task_type = Column(String(50), nullable=False)
    assigned_staff = Column(String(100))
    status = Column(String(30), nullable=False, default=TaskStatus.PENDING.value)
    priority = Column(String(20), nullable=False, default="NORMAL")
    scheduled_for = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    cleaning_notes = Column(Text)
    damaged_item_notes = Column(Text)
    missing_item_notes = Column(Text)
    supplies_replaced = Column(JSON)  # list of dicts {item_id, name, qty}
    linked_complaint_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
