from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal
import uuid

class GradeBase(BaseModel):
    enrollment_id: uuid.UUID
    assessment_id: uuid.UUID
    score: Decimal
    
    @validator('score')
    def score_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Score must be positive')
        return v

class GradeCreate(GradeBase):
    recorded_by: Optional[uuid.UUID] = None

class GradeUpdate(BaseModel):
    score: Decimal
    recorded_by: Optional[uuid.UUID] = None

class GradeResponse(GradeBase):
    id: uuid.UUID
    recorded_by: Optional[uuid.UUID] = None
    recorded_at: datetime
    
    class Config:
        from_attributes = True

class GradeWithDetails(GradeResponse):
    enrollment: "EnrollmentResponse"
    assessment: "AssessmentResponse"
    
    class Config:
        from_attributes = True
