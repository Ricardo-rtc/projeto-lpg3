from pydantic import BaseModel
from typing import Optional
import uuid

class DisciplineBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    credits: Optional[int] = None

class DisciplineCreate(DisciplineBase):
    pass

class DisciplineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None

class DisciplineResponse(DisciplineBase):
    id: uuid.UUID
    
    class Config:
        from_attributes = True
