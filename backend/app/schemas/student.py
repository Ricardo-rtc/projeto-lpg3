from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

class StudentBase(BaseModel):
    registration_number: Optional[str] = None
    enrollment_date: Optional[date] = None
    birth_date: Optional[date] = None
    active: bool = True

class StudentCreate(StudentBase):
    user_id: uuid.UUID

class StudentUpdate(BaseModel):
    registration_number: Optional[str] = None
    birth_date: Optional[date] = None
    active: Optional[bool] = None

class StudentResponse(StudentBase):
    id: uuid.UUID
    user_id: uuid.UUID
    
    class Config:
        from_attributes = True

class StudentWithUser(StudentResponse):
    user: "UserResponse"
    
    class Config:
        from_attributes = True
