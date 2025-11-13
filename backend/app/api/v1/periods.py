from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.core.database import get_db
from app.schemas.period import PeriodCreate, PeriodResponse, PeriodUpdate
from app.services.period import PeriodService
from app.api.deps import get_current_admin, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=PeriodResponse, status_code=status.HTTP_201_CREATED)
def create_period(
    period: PeriodCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Criar novo período (apenas admin)"""
    service = PeriodService(db)
    return service.create_period(period)

@router.get("/{period_id}", response_model=PeriodResponse)
def get_period(
    period_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter período por ID"""
    service = PeriodService(db)
    period = service.get_by_id(period_id)
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found"
        )
    return period

@router.get("/", response_model=List[PeriodResponse])
def list_periods(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar períodos"""
    service = PeriodService(db)
    if active_only:
        return service.get_active_periods()
    return service.get_all(skip, limit)

@router.put("/{period_id}", response_model=PeriodResponse)
def update_period(
    period_id: uuid.UUID,
    period_data: PeriodUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Atualizar período (apenas admin)"""
    service = PeriodService(db)
    period = service.update_period(period_id, period_data)
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found"
        )
    return period

@router.delete("/{period_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_period(
    period_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Deletar período (apenas admin)"""
    service = PeriodService(db)
    if not service.delete_period(period_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found"
        )
