from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

class PeriodBase(BaseModel):
    code: str
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    active: bool = True

class PeriodCreate(PeriodBase):
    pass

class PeriodUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    active: Optional[bool] = None

class PeriodResponse(PeriodBase):
    id: uuid.UUID
    
    class Config:
        from_attributes = True
