from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.core.database import get_db
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.services.student import StudentService
from app.api.deps import get_current_admin, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student: StudentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Criar novo estudante (apenas admin)"""
    service = StudentService(db)
    return service.create_student(student)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter estudante por ID"""
    service = StudentService(db)
    student = service.get_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

@router.get("/", response_model=List[StudentResponse])
def list_students(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar estudantes"""
    service = StudentService(db)
    if active_only:
        return service.get_active_students()
    return service.get_all(skip, limit)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: uuid.UUID,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Atualizar estudante (apenas admin)"""
    service = StudentService(db)
    student = service.update_student(student_id, student_data)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Deletar estudante (apenas admin)"""
    service = StudentService(db)
    if not service.delete_student(student_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
