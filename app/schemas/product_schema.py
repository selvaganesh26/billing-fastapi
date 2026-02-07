from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    stock: int = Field(gt=0)
    price: float = Field(gt=0)
    tax_percent: float = Field(ge=0)
