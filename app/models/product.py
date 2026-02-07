from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    stock = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=False)
    tax_percent = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    purchase_items = relationship("PurchaseItem", back_populates="product", lazy="select")
    
    __table_args__ = (
        CheckConstraint('stock >= 0', name='check_stock_positive'),
        CheckConstraint('price > 0', name='check_price_positive'),
        CheckConstraint('tax_percent >= 0', name='check_tax_positive'),
        Index('idx_product_name', 'name'),
    )
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', stock={self.stock})>"
