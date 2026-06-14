"""SQLAlchemy model for damage_reports table.

Matches the Alembic migration 0006_create_damage_reports_table.py.
"""

import uuid
from sqlalchemy import Column, String, Text, DateTime, Boolean, Numeric, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from app.models import Base
from app.shared.enums import DamageReportStatus, DamageType

class DamageReportModel(Base):
    __tablename__ = "damage_reports"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = Column(String(50), nullable=False)
    task_id = Column(PG_UUID(as_uuid=True), nullable=True)
    booking_ref = Column(String(100), nullable=True)
    item_description = Column(String(500), nullable=False)
    damage_type = Column(String(30), nullable=False)  # Could use Enum(DamageType) if desired
    reported_by = Column(String(100), nullable=False)
    is_guest_chargeable = Column(Boolean, nullable=False, server_default="FALSE")
    requires_repair = Column(Boolean, nullable=False, server_default="FALSE")
    estimated_cost = Column(Numeric(10, 2), nullable=True)
    status = Column(String(30), nullable=False, server_default=DamageReportStatus.OPEN.value)
    photo_urls = Column(ARRAY(Text), nullable=True)
    maintenance_request_id = Column(String(100), nullable=True)
    invoice_charge_id = Column(String(100), nullable=True)
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
