from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

class TeacherBase(BaseModel):
    employee_number: Optional[str] = None
    hire_date: Optional[date] = None

class TeacherCreate(TeacherBase):
    user_id: uuid.UUID

class TeacherUpdate(BaseModel):
    employee_number: Optional[str] = None
    hire_date: Optional[date] = None

class TeacherResponse(TeacherBase):
    id: uuid.UUID
    user_id: uuid.UUID
    
    class Config:
        from_attributes = True

class TeacherWithUser(TeacherResponse):
    user: "UserResponse"
    
    class Config:
        from_attributes = True
