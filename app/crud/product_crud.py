from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product_schema import ProductCreate


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product
