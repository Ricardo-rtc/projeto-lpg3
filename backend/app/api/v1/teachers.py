from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.core.database import get_db
from app.schemas.teacher import TeacherCreate, TeacherResponse, TeacherUpdate
from app.services.teacher import TeacherService
from app.api.deps import get_current_admin, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(
    teacher: TeacherCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Criar novo professor (apenas admin)"""
    service = TeacherService(db)
    return service.create_teacher(teacher)

@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(
    teacher_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter professor por ID"""
    service = TeacherService(db)
    teacher = service.get_by_id(teacher_id)
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    return teacher

@router.get("/", response_model=List[TeacherResponse])
def list_teachers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar professores"""
    service = TeacherService(db)
    return service.get_all(skip, limit)

@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(
    teacher_id: uuid.UUID,
    teacher_data: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Atualizar professor (apenas admin)"""
    service = TeacherService(db)
    teacher = service.update_teacher(teacher_id, teacher_data)
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    return teacher

@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(
    teacher_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Deletar professor (apenas admin)"""
    service = TeacherService(db)
    if not service.delete_teacher(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
