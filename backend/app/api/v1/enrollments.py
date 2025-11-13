from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse, EnrollmentUpdate
from app.services.enrollment import EnrollmentService
from app.api.deps import get_current_admin, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(
    enrollment: EnrollmentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Matricular aluno em turma (apenas admin)"""
    service = EnrollmentService(db)
    try:
        return service.enroll_student(enrollment)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(
    enrollment_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter matrícula por ID"""
    service = EnrollmentService(db)
    enrollment = service.get_by_id(enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return enrollment

@router.get("/", response_model=List[EnrollmentResponse])
def list_enrollments(
    skip: int = 0,
    limit: int = 100,
    student_id: Optional[uuid.UUID] = Query(None),
    class_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar matrículas com filtros opcionais"""
    service = EnrollmentService(db)
    
    if student_id:
        return service.get_by_student(student_id)
    elif class_id:
        return service.get_by_class(class_id)
    
    return service.get_all(skip, limit)

@router.put("/{enrollment_id}", response_model=EnrollmentResponse)
def update_enrollment(
    enrollment_id: uuid.UUID,
    enrollment_data: EnrollmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Atualizar matrícula (apenas admin)"""
    service = EnrollmentService(db)
    enrollment = service.update_enrollment(enrollment_id, enrollment_data)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return enrollment

@router.post("/{enrollment_id}/calculate-average")
def calculate_average(
    enrollment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calcular média final da matrícula"""
    service = EnrollmentService(db)
    try:
        average = service.calculate_final_average(enrollment_id)
        return {"enrollment_id": enrollment_id, "final_average": float(average)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(
    enrollment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Deletar matrícula (apenas admin)"""
    service = EnrollmentService(db)
    if not service.delete_enrollment(enrollment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
