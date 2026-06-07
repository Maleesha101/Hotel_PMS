"""Custom exception classes for the housekeeping service.

These exceptions are used throughout the service and are mapped to HTTP
responses in ``app.main``.
"""

class ResourceNotFoundException(Exception):
    """Raised when a requested database record cannot be found."""

    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail
        super().__init__(detail)

class InvalidStateException(Exception):
    """Raised when an operation would violate a business rule or state transition."""

    def __init__(self, detail: str = "Invalid state for operation"):
        self.detail = detail
        super().__init__(detail)

class InsufficientStockException(Exception):
    """Raised when an inventory deduction would result in negative stock."""

    def __init__(self, item_name: str, available: int):
        self.item_name = item_name
        self.available = available
        self.detail = f"Insufficient stock for item {item_name}. Available: {available}."
        super().__init__(self.detail)
