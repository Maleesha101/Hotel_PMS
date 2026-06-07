"""SQLAlchemy model for room_supply_standards table."""

import uuid
from sqlalchemy import Column, String, Text, SmallInteger, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from app.models import Base

class RoomSupplyStandardModel(Base):
    __tablename__ = "room_supply_standards"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_type = Column(String(50), nullable=False)
    item_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    quantity = Column(SmallInteger, nullable=False, server_default="1")
    unit = Column(String(30))
    is_active = Column(Boolean, nullable=False, server_default=func.true())
    notes = Column(Text)
    created_at = Column("created_at", func.now(), nullable=False)
    updated_at = Column("updated_at", func.now(), nullable=False)
    __table_args__ = (UniqueConstraint("room_type", "item_name", name="uq_room_type_item_name"),)
