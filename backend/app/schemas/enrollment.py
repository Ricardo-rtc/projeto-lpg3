from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
import uuid
from app.models.enrollment import EnrollmentStatus

class EnrollmentBase(BaseModel):
    student_id: uuid.UUID
    class_id: uuid.UUID
    status: EnrollmentStatus = EnrollmentStatus.MATRICULADO

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    status: Optional[EnrollmentStatus] = None
    final_average: Optional[Decimal] = None

class EnrollmentResponse(EnrollmentBase):
    id: uuid.UUID
    enrolled_at: datetime
    final_average: Optional[Decimal] = None
    
    class Config:
        from_attributes = True

class EnrollmentWithDetails(EnrollmentResponse):
    student: "StudentResponse"
    class_: "ClassResponse"
    
    class Config:
        from_attributes = True
