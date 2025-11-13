from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
import uuid

class AssessmentBase(BaseModel):
    class_id: uuid.UUID
    name: str
    description: Optional[str] = None
    date: Optional[date] = None
    weight: Decimal = Decimal("1.0")
    max_score: Decimal = Decimal("100")

class AssessmentCreate(AssessmentBase):
    pass

class AssessmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    weight: Optional[Decimal] = None
    max_score: Optional[Decimal] = None

class AssessmentResponse(AssessmentBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
