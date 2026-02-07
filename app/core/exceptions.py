from typing import Any, Optional


class BillingException(Exception):
    """Base exception for billing system"""
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class ResourceNotFoundException(BillingException):
    """Raised when a resource is not found"""
    pass


class InsufficientStockException(BillingException):
    """Raised when product stock is insufficient"""
    pass


class InvalidPaymentException(BillingException):
    """Raised when payment amount is invalid"""
    pass


class InsufficientDenominationException(BillingException):
    """Raised when denomination stock is insufficient"""
    pass
