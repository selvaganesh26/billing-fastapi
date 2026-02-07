from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models.purchase import Purchase
from app.core.exceptions import ResourceNotFoundException
import logging

logger = logging.getLogger(__name__)


class PurchaseRepository:
    """Repository pattern for Purchase operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, purchase_id: int) -> Optional[Purchase]:
        """Get purchase by ID with all relationships loaded"""
        return (
            self.db.query(Purchase)
            .options(
                joinedload(Purchase.customer),
                joinedload(Purchase.purchase_items),
                joinedload(Purchase.purchase_denominations)
            )
            .filter(Purchase.id == purchase_id)
            .first()
        )
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Purchase]:
        """Get all purchases with pagination"""
        return (
            self.db.query(Purchase)
            .options(joinedload(Purchase.customer))
            .order_by(Purchase.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_customer_email(self, email: str, skip: int = 0, limit: int = 100) -> List[Purchase]:
        """Get purchases by customer email"""
        return (
            self.db.query(Purchase)
            .join(Purchase.customer)
            .filter(Purchase.customer.has(email=email))
            .order_by(Purchase.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count(self) -> int:
        """Get total purchase count"""
        return self.db.query(Purchase).count()
