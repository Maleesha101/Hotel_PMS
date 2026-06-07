"""SQLAlchemy model for inventory_items table."""

import uuid
from sqlalchemy import Column, String, Integer, Numeric, Boolean, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from app.models import Base

class InventoryItemModel(Base):
    __tablename__ = "inventory_items"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    sku = Column(String(100), unique=True)
    available_qty = Column(Integer, nullable=False, server_default="0")
    min_stock_level = Column(Integer, nullable=False, server_default="5")
    unit = Column(String(30))
    unit_cost = Column(Numeric(10, 2))
    supplier_name = Column(String(255))
    supplier_contact = Column(String(255))
    location = Column(String(100))
    is_active = Column(Boolean, nullable=False, server_default=func.true())
    last_restocked_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
