from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.schemas import DenominationCreate, DenominationUpdate, DenominationResponse
from app.crud.denomination_repository import DenominationRepository
from app.core.exceptions import ResourceNotFoundException

router = APIRouter(prefix="/denominations", tags=["Denominations"])


@router.post("/", response_model=DenominationResponse, status_code=status.HTTP_201_CREATED)
def create_denomination(denom: DenominationCreate, db: Session = Depends(get_db)):
    """Create a new denomination"""
    try:
        repo = DenominationRepository(db)
        return repo.create(denom)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[DenominationResponse])
def get_denominations(db: Session = Depends(get_db)):
    """Get all denominations"""
    repo = DenominationRepository(db)
    return repo.get_all()


@router.get("/{value}", response_model=DenominationResponse)
def get_denomination(value: int, db: Session = Depends(get_db)):
    """Get denomination by value"""
    repo = DenominationRepository(db)
    denom = repo.get_by_value(value)
    if not denom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Denomination not found")
    return denom


@router.put("/{value}", response_model=DenominationResponse)
def update_denomination(value: int, denom: DenominationUpdate, db: Session = Depends(get_db)):
    """Update denomination count"""
    try:
        repo = DenominationRepository(db)
        return repo.update(value, denom)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete("/{value}", status_code=status.HTTP_204_NO_CONTENT)
def delete_denomination(value: int, db: Session = Depends(get_db)):
    """Delete denomination"""
    try:
        repo = DenominationRepository(db)
        repo.delete(value)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
