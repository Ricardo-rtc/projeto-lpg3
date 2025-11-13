from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.schemas.assessment import AssessmentCreate, AssessmentResponse, AssessmentUpdate
from app.services.assessment import AssessmentService
from app.api.deps import get_current_teacher, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
def create_assessment(
    assessment: AssessmentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    """Criar nova avaliação (professores e admin)"""
    service = AssessmentService(db)
    return service.create_assessment(assessment)

@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment(
    assessment_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter avaliação por ID"""
    service = AssessmentService(db)
    assessment = service.get_by_id(assessment_id)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    return assessment

@router.get("/", response_model=List[AssessmentResponse])
def list_assessments(
    skip: int = 0,
    limit: int = 100,
    class_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar avaliações"""
    service = AssessmentService(db)
    
    if class_id:
        return service.get_by_class(class_id)
    
    return service.get_all(skip, limit)

@router.put("/{assessment_id}", response_model=AssessmentResponse)
def update_assessment(
    assessment_id: uuid.UUID,
    assessment_data: AssessmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    """Atualizar avaliação (professores e admin)"""
    service = AssessmentService(db)
    assessment = service.update_assessment(assessment_id, assessment_data)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    return assessment

@router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assessment(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    """Deletar avaliação (professores e admin)"""
    service = AssessmentService(db)
    if not service.delete_assessment(assessment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
