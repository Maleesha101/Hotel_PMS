"""Shared enumeration definitions for the housekeeping service."""

from enum import Enum

class RoomStatus(str, Enum):
    CLEAN = "CLEAN"
    DIRTY = "DIRTY"
    OCCUPIED = "OCCUPIED"
    VACANT = "VACANT"
    OUT_OF_ORDER = "OUT_OF_ORDER"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"

class TaskType(str, Enum):
    CHECKOUT_CLEAN = "CHECKOUT_CLEAN"
    ROUTINE_CLEAN = "ROUTINE_CLEAN"
    DEEP_CLEAN = "DEEP_CLEAN"
    INSPECTION = "INSPECTION"
    TURNDOWN = "TURNDOWN"

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    NEEDS_MAINTENANCE = "NEEDS_MAINTENANCE"

class InventoryCategory(str, Enum):
    ROOM_SUPPLIES = "ROOM_SUPPLIES"
    CLEANING = "CLEANING"
    LINEN = "LINEN"
    BATHROOM = "BATHROOM"
    MINIBAR = "MINIBAR"
    MAINTENANCE_PARTS = "MAINTENANCE_PARTS"
    OFFICE = "OFFICE"

class TransactionType(str, Enum):
    ISSUE = "ISSUE"
    ADD = "ADD"
    ADJUSTMENT = "ADJUSTMENT"
    DAMAGE = "DAMAGE"
    WASTAGE = "WASTAGE"

class DamageType(str, Enum):
    DAMAGED = "DAMAGED"
    MISSING = "MISSING"
    STAINED = "STAINED"
    BROKEN = "BROKEN"

class DamageReportStatus(str, Enum):
    OPEN = "OPEN"
    SENT_TO_MAINTENANCE = "SENT_TO_MAINTENANCE"
    SENT_TO_INVOICE = "SENT_TO_INVOICE"
    RESOLVED = "RESOLVED"
    WAIVED = "WAIVED"
