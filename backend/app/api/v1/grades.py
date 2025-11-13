from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.schemas.grade import GradeCreate, GradeResponse, GradeUpdate
from app.services.grade import GradeService
from app.api.deps import get_current_teacher, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
def create_grade(
    grade: GradeCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    """Registrar nota (professores e admin)"""
    service = GradeService(db)
    try:
        return service.create_grade(grade)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{grade_id}", response_model=GradeResponse)
def get_grade(
    grade_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter nota por ID"""
    service = GradeService(db)
    grade = service.get_by_id(grade_id)
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )
    return grade

@router.get("/", response_model=List[GradeResponse])
def list_grades(
    skip: int = 0,
    limit: int = 100,
    enrollment_id: Optional[uuid.UUID] = Query(None),
    assessment_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar notas com filtros opcionais"""
    service = GradeService(db)
    
    if enrollment_id:
        return service.get_by_enrollment(enrollment_id)
    elif assessment_id:
        return service.get_by_assessment(assessment_id)
    
    return service.get_all(skip, limit)

@router.put("/{grade_id}", response_model=GradeResponse)
def update_grade(
    grade_id: uuid.UUID,
    grade_data: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    """Atualizar nota (professores e admin)"""
    service = GradeService(db)
    grade = service.update_grade(grade_id, grade_data)
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )
    return grade

@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(
    grade_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    """Deletar nota (professores e admin)"""
    service = GradeService(db)
    if not service.delete_grade(grade_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )
