from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.schemas import PurchaseCreate, PurchaseResponse
from app.services.billing_service import BillingService
from app.crud.purchase_repository import PurchaseRepository
from app.core.exceptions import (
    ResourceNotFoundException,
    InsufficientStockException,
    InvalidPaymentException,
    InsufficientDenominationException
)

router = APIRouter(prefix="/purchases", tags=["Purchases"])


@router.post("/", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    """
    Create a new purchase (Generate Bill).
    
    This endpoint handles the complete billing flow:
    1. Validates customer
    2. Validates products and stock
    3. Calculates totals with tax
    4. Creates purchase with items
    5. Updates inventory
    6. Handles change denominations
    
    All operations are wrapped in a database transaction.
    """
    try:
        service = BillingService(db)
        return service.create_purchase(purchase)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except InsufficientStockException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except InvalidPaymentException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except InsufficientDenominationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[PurchaseResponse])
def get_purchases(
    customer_email: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all purchases with optional customer email filter and pagination"""
    repo = PurchaseRepository(db)
    if customer_email:
        return repo.get_by_customer_email(customer_email, skip=skip, limit=limit)
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(purchase_id: int, db: Session = Depends(get_db)):
    """Get purchase by ID with all details"""
    repo = PurchaseRepository(db)
    purchase = repo.get_by_id(purchase_id)
    if not purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
    return purchase
