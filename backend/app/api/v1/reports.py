from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from typing import List
from app.core.database import get_db
from app.schemas.report import StudentGradeReport, DisciplinePerformanceReport, PeriodReport
from app.services.report import ReportService
from app.api.deps import get_current_user, get_current_teacher
from app.models.user import User

router = APIRouter()

@router.get("/student/{student_id}/grades", response_model=List[StudentGradeReport])
def get_student_grades_report(
    student_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Relatório de notas do aluno"""
    service = ReportService(db)
    try:
        return service.get_student_grades_report(student_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/discipline/{discipline_id}/performance", response_model=DisciplinePerformanceReport)
def get_discipline_performance_report(
    discipline_id: uuid.UUID,
    period_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    """Relatório de desempenho da disciplina (professores e admin)"""
    service = ReportService(db)
    try:
        return service.get_discipline_performance_report(discipline_id, period_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/period/{period_id}", response_model=PeriodReport)
def get_period_report(
    period_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    """Relatório geral do período (professores e admin)"""
    service = ReportService(db)
    try:
        return service.get_period_report(period_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
