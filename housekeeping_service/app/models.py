from sqlalchemy import Column, String, Integer, Boolean, text, ForeignKey, DateTime, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import DeclarativeBase, mapped_column
import uuid

class Base(DeclarativeBase):
    pass

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = mapped_column(String(255), nullable=False)
    current_balance = mapped_column(Integer, default=0)

class RoomSupplyStandard(Base):
    __tablename__ = "room_supply_standards"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_type = mapped_column(String(50), nullable=False)
    item_id = mapped_column(UUID(as_uuid=True), ForeignKey("inventory_items.id"), nullable=False)
    quantity = mapped_column(Integer, nullable=False)

class HousekeepingTask(Base):
    __tablename__ = "housekeeping_tasks"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = mapped_column(String(50), nullable=False)
    room_type = mapped_column(String(50), nullable=False)
    type = mapped_column(String(50), nullable=False)  # e.g., CHECKOUT_CLEAN
    status = mapped_column(String(50), nullable=False, default="PENDING")
    created_at = mapped_column(DateTime(timezone=True), server_default=text("NOW()"), nullable=False)

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    item_id = mapped_column(UUID(as_uuid=True), ForeignKey("inventory_items.id"), nullable=False)
    transaction_type = mapped_column(String(20), nullable=False)  # ISSUE, RECEIVE
    quantity = mapped_column(Integer, nullable=False)
    balance_after = mapped_column(Integer, nullable=False)
    room_id = mapped_column(String(50))
    task_id = mapped_column(UUID(as_uuid=True), ForeignKey("housekeeping_tasks.id"), nullable=True)
    performed_by = mapped_column(String(100))
    notes = mapped_column(Text())
    created_at = mapped_column(DateTime(timezone=True), server_default=text("NOW()"), nullable=False)

class DamageReport(Base):
    __tablename__ = "damage_reports"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    room_id = mapped_column(String(50), nullable=False)
    task_id = mapped_column(UUID(as_uuid=True), ForeignKey("housekeeping_tasks.id"), nullable=True)
    booking_ref = mapped_column(String(100))
    item_description = mapped_column(String(500), nullable=False)
    damage_type = mapped_column(String(30), nullable=False)
    reported_by = mapped_column(String(100), nullable=False)
    is_guest_chargeable = mapped_column(Boolean, nullable=False, server_default=text("FALSE"))
    requires_repair = mapped_column(Boolean, nullable=False, server_default=text("FALSE"))
    estimated_cost = mapped_column(Numeric(10, 2))
    status = mapped_column(String(30), nullable=False, server_default="OPEN")
    photo_urls = mapped_column(ARRAY(Text))
    maintenance_request_id = mapped_column(String(100))
    invoice_charge_id = mapped_column(String(100))
    admin_notes = mapped_column(Text())
    created_at = mapped_column(DateTime(timezone=True), server_default=text("NOW()"), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=text("NOW()"), nullable=False)