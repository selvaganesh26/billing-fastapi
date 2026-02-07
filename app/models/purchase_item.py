from sqlalchemy import Column, Integer, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.database import Base


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price_snapshot = Column(Float, nullable=False)
    tax_percent_snapshot = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Relationships
    purchase = relationship("Purchase", back_populates="purchase_items")
    product = relationship("Product", back_populates="purchase_items")
    
    __table_args__ = (
        Index('idx_purchase_item_purchase', 'purchase_id'),
        Index('idx_purchase_item_product', 'product_id'),
    )
    
    def __repr__(self):
        return f"<PurchaseItem(id={self.id}, purchase_id={self.purchase_id}, product_id={self.product_id}, qty={self.quantity})>"
