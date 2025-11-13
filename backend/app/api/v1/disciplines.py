from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.core.database import get_db
from app.schemas.discipline import DisciplineCreate, DisciplineResponse, DisciplineUpdate
from app.services.discipline import DisciplineService
from app.api.deps import get_current_admin, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=DisciplineResponse, status_code=status.HTTP_201_CREATED)
def create_discipline(
    discipline: DisciplineCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Criar nova disciplina (apenas admin)"""
    service = DisciplineService(db)
    return service.create_discipline(discipline)

@router.get("/{discipline_id}", response_model=DisciplineResponse)
def get_discipline(
    discipline_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter disciplina por ID"""
    service = DisciplineService(db)
    discipline = service.get_by_id(discipline_id)
    if not discipline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discipline not found"
        )
    return discipline

@router.get("/", response_model=List[DisciplineResponse])
def list_disciplines(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar disciplinas"""
    service = DisciplineService(db)
    return service.get_all(skip, limit)

@router.put("/{discipline_id}", response_model=DisciplineResponse)
def update_discipline(
    discipline_id: uuid.UUID,
    discipline_data: DisciplineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Atualizar disciplina (apenas admin)"""
    service = DisciplineService(db)
    discipline = service.update_discipline(discipline_id, discipline_data)
    if not discipline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discipline not found"
        )
    return discipline

@router.delete("/{discipline_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_discipline(
    discipline_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Deletar disciplina (apenas admin)"""
    service = DisciplineService(db)
    if not service.delete_discipline(discipline_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discipline not found"
        )
