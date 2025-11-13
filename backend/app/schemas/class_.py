from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class ClassBase(BaseModel):
    discipline_id: uuid.UUID
    period_id: uuid.UUID
    teacher_id: Optional[uuid.UUID] = None
    code: Optional[str] = None
    capacity: Optional[int] = None

class ClassCreate(ClassBase):
    pass

class ClassUpdate(BaseModel):
    teacher_id: Optional[uuid.UUID] = None
    code: Optional[str] = None
    capacity: Optional[int] = None

class ClassResponse(ClassBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class ClassWithDetails(ClassResponse):
    discipline: "DisciplineResponse"
    period: "PeriodResponse"
    teacher: Optional["TeacherResponse"] = None
    
    class Config:
        from_attributes = True
