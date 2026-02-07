from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.database import Base


class PurchaseDenomination(Base):
    __tablename__ = "purchase_denominations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id", ondelete="CASCADE"), nullable=False)
    denomination_value = Column(Integer, nullable=False)
    count_given = Column(Integer, nullable=False)
    
    # Relationships
    purchase = relationship("Purchase", back_populates="purchase_denominations")
    
    __table_args__ = (
        Index('idx_purchase_denomination_purchase', 'purchase_id'),
    )
    
    def __repr__(self):
        return f"<PurchaseDenomination(purchase_id={self.purchase_id}, value={self.denomination_value}, count={self.count_given})>"
