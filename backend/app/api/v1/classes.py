from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.schemas.class_ import ClassCreate, ClassResponse, ClassUpdate
from app.services.class_ import ClassService
from app.api.deps import get_current_admin, get_current_teacher, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(
    class_data: ClassCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Criar nova turma (apenas admin)"""
    service = ClassService(db)
    return service.create_class(class_data)

@router.get("/{class_id}", response_model=ClassResponse)
def get_class(
    class_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter turma por ID"""
    service = ClassService(db)
    class_obj = service.get_by_id(class_id)
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    return class_obj

@router.get("/", response_model=List[ClassResponse])
def list_classes(
    skip: int = 0,
    limit: int = 100,
    period_id: Optional[uuid.UUID] = Query(None),
    teacher_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar turmas com filtros opcionais"""
    service = ClassService(db)
    
    if period_id:
        return service.get_by_period(period_id)
    elif teacher_id:
        return service.get_by_teacher(teacher_id)
    
    return service.get_all(skip, limit)

@router.put("/{class_id}", response_model=ClassResponse)
def update_class(
    class_id: uuid.UUID,
    class_data: ClassUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Atualizar turma (apenas admin)"""
    service = ClassService(db)
    class_obj = service.update_class(class_id, class_data)
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    return class_obj

@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(
    class_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Deletar turma (apenas admin)"""
    service = ClassService(db)
    if not service.delete_class(class_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
