from sqlalchemy import Column, Integer, DateTime, CheckConstraint, Index
from datetime import datetime
from app.db.database import Base


class Denomination(Base):
    __tablename__ = "denominations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(Integer, unique=True, nullable=False)
    available_count = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        CheckConstraint('value > 0', name='check_value_positive'),
        CheckConstraint('available_count >= 0', name='check_count_positive'),
        Index('idx_denomination_value', 'value'),
    )
    
    def __repr__(self):
        return f"<Denomination(value={self.value}, count={self.available_count})>"
