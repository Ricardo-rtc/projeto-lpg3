from sqlalchemy.orm import Session
from typing import List
import uuid
from app.models.assessment import Assessment
from .base import BaseRepository

class AssessmentRepository(BaseRepository[Assessment]):
    def __init__(self, db: Session):
        super().__init__(Assessment, db)
    
    def get_by_class(self, class_id: uuid.UUID) -> List[Assessment]:
        return self.db.query(Assessment).filter(
            Assessment.class_id == class_id
        ).all()
