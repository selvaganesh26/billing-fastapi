from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from app.models.product import Product
from app.schemas.schemas import ProductCreate, ProductUpdate
from app.core.exceptions import ResourceNotFoundException
import logging

logger = logging.getLogger(__name__)


class ProductRepository:
    """Repository pattern for Product operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, product_data: ProductCreate) -> Product:
        """Create a new product"""
        try:
            product = Product(**product_data.model_dump())
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            logger.info(f"Product created: {product.name}")
            return product
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"Product with name '{product_data.name}' already exists")
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get all products with pagination"""
        return self.db.query(Product).offset(skip).limit(limit).all()
    
    def update(self, product_id: int, product_data: ProductUpdate) -> Product:
        """Update product"""
        product = self.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundException(f"Product with ID {product_id} not found")
        
        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        self.db.commit()
        self.db.refresh(product)
        logger.info(f"Product updated: {product.name}")
        return product
    
    def delete(self, product_id: int) -> bool:
        """Delete product"""
        product = self.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundException(f"Product with ID {product_id} not found")
        
        self.db.delete(product)
        self.db.commit()
        logger.info(f"Product deleted: {product.name}")
        return True
    
    def count(self) -> int:
        """Get total product count"""
        return self.db.query(Product).count()
