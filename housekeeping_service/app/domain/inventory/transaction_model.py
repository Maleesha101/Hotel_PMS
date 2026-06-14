"""SQLAlchemy model for inventory_transactions table."""

import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from app.models import Base
from app.shared.enums import TransactionType

class InventoryTransactionModel(Base):
    __tablename__ = "inventory_transactions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(PG_UUID(as_uuid=True), ForeignKey("inventory_items.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType, create_type=False), nullable=False)
    quantity = Column(Integer, nullable=False)
    balance_after = Column(Integer, nullable=False)
    room_id = Column(String(50), nullable=True)
    task_id = Column(PG_UUID(as_uuid=True), ForeignKey("housekeeping_tasks.id"), nullable=True)
    performed_by = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
