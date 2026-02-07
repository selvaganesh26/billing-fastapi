from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    purchases = relationship("Purchase", back_populates="customer", lazy="select")
    
    __table_args__ = (
        Index('idx_customer_email', 'email'),
    )
    
    def __repr__(self):
        return f"<Customer(id={self.id}, email='{self.email}')>"
