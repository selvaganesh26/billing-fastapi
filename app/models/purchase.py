from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    total_amount = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)
    final_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    balance_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    customer = relationship("Customer", back_populates="purchases")
    purchase_items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan", lazy="select")
    purchase_denominations = relationship("PurchaseDenomination", back_populates="purchase", cascade="all, delete-orphan", lazy="select")
    
    __table_args__ = (
        Index('idx_purchase_customer', 'customer_id'),
        Index('idx_purchase_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Purchase(id={self.id}, customer_id={self.customer_id}, final_amount={self.final_amount})>"
