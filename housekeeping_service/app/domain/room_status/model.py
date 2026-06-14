"""SQLAlchemy model for room_status table."""

from sqlalchemy import Column, String, Text, DateTime, SmallInteger, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.models import Base
from app.shared.enums import RoomStatus
import uuid

class RoomStatusModel(Base):
    __tablename__ = "room_status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = Column(String(50), nullable=False, unique=True)
    room_number = Column(String(20), nullable=False)
    floor = Column(SmallInteger)
    room_type = Column(String(50))
    status = Column(Enum(RoomStatus), nullable=False, default=RoomStatus.VACANT)
    previous_status = Column(Enum(RoomStatus))
    updated_by = Column(String(100))
    status_note = Column(Text)
    last_checkout = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
