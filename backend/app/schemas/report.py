from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date
import uuid

class StudentGradeReport(BaseModel):
    student_id: uuid.UUID
    student_name: str
    registration_number: Optional[str]
    class_code: Optional[str]
    discipline_name: str
    assessments: List[dict]
    final_average: Optional[Decimal]
    status: str

class DisciplinePerformanceReport(BaseModel):
    discipline_id: uuid.UUID
    discipline_name: str
    period_name: str
    total_students: int
    average_grade: Optional[Decimal]
    approval_rate: Optional[Decimal]

class PeriodReport(BaseModel):
    period_id: uuid.UUID
    period_name: str
    start_date: Optional[date]
    end_date: Optional[date]
    total_classes: int
    total_students: int
    total_disciplines: int
