from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from app.models.denomination import Denomination
from app.schemas.schemas import DenominationCreate, DenominationUpdate
from app.core.exceptions import ResourceNotFoundException
import logging

logger = logging.getLogger(__name__)


class DenominationRepository:
    """Repository pattern for Denomination operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, denom_data: DenominationCreate) -> Denomination:
        """Create a new denomination"""
        try:
            denomination = Denomination(**denom_data.model_dump())
            self.db.add(denomination)
            self.db.commit()
            self.db.refresh(denomination)
            logger.info(f"Denomination created: {denomination.value}")
            return denomination
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"Denomination with value {denom_data.value} already exists")
    
    def get_by_value(self, value: int) -> Optional[Denomination]:
        """Get denomination by value"""
        return self.db.query(Denomination).filter(Denomination.value == value).first()
    
    def get_all(self) -> List[Denomination]:
        """Get all denominations"""
        return self.db.query(Denomination).order_by(Denomination.value.desc()).all()
    
    def update(self, value: int, denom_data: DenominationUpdate) -> Denomination:
        """Update denomination count"""
        denomination = self.get_by_value(value)
        if not denomination:
            raise ResourceNotFoundException(f"Denomination with value {value} not found")
        
        denomination.available_count = denom_data.available_count
        self.db.commit()
        self.db.refresh(denomination)
        logger.info(f"Denomination updated: {value} -> count: {denom_data.available_count}")
        return denomination
    
    def delete(self, value: int) -> bool:
        """Delete denomination"""
        denomination = self.get_by_value(value)
        if not denomination:
            raise ResourceNotFoundException(f"Denomination with value {value} not found")
        
        self.db.delete(denomination)
        self.db.commit()
        logger.info(f"Denomination deleted: {value}")
        return True
