from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional, Any
from datetime import datetime


# Customer Schemas
class CustomerBase(BaseModel):
    email: EmailStr


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Product Schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    stock: int = Field(..., ge=0)
    price: float = Field(..., gt=0)
    tax_percent: float = Field(..., ge=0, le=100)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    stock: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, gt=0)
    tax_percent: Optional[float] = Field(None, ge=0, le=100)


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Denomination Schemas
class DenominationBase(BaseModel):
    value: int = Field(..., gt=0)
    available_count: int = Field(..., ge=0)


class DenominationCreate(DenominationBase):
    pass


class DenominationUpdate(BaseModel):
    available_count: int = Field(..., ge=0)


class DenominationResponse(DenominationBase):
    id: int
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Purchase Item Schema
class PurchaseItemInput(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class PurchaseItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price_snapshot: float
    tax_percent_snapshot: float
    tax_amount: float
    total_price: float
    
    model_config = ConfigDict(from_attributes=True)


# Denomination Input for Purchase
class DenominationInput(BaseModel):
    value: int = Field(..., gt=0)
    count: int = Field(..., ge=0)


# Purchase Schemas
class PurchaseCreate(BaseModel):
    customer_email: EmailStr
    items: List[PurchaseItemInput] = Field(..., min_length=1)
    paid_amount: float = Field(..., gt=0)
    denominations: List[DenominationInput] = Field(..., min_length=1)


class PurchaseDenominationResponse(BaseModel):
    denomination_value: int
    count_given: int
    
    model_config = ConfigDict(from_attributes=True)


class PurchaseResponse(BaseModel):
    id: int
    customer_id: int
    total_amount: float
    tax_amount: float
    final_amount: float
    paid_amount: float
    balance_amount: float
    created_at: datetime
    purchase_items: List[PurchaseItemResponse] = []
    change_denominations: List[PurchaseDenominationResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


# Pagination
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
