from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import uuid
from app.models.grade import Grade
from .base import BaseRepository

class GradeRepository(BaseRepository[Grade]):
    def __init__(self, db: Session):
        super().__init__(Grade, db)
    
    def get_by_enrollment(self, enrollment_id: uuid.UUID) -> List[Grade]:
        return self.db.query(Grade).filter(
            Grade.enrollment_id == enrollment_id
        ).all()
    
    def get_by_assessment(self, assessment_id: uuid.UUID) -> List[Grade]:
        return self.db.query(Grade).filter(
            Grade.assessment_id == assessment_id
        ).all()
    
    def get_grade(self, enrollment_id: uuid.UUID, assessment_id: uuid.UUID) -> Optional[Grade]:
        return self.db.query(Grade).filter(
            Grade.enrollment_id == enrollment_id,
            Grade.assessment_id == assessment_id
        ).first()
    
    def get_with_details(self, grade_id: uuid.UUID):
        return self.db.query(Grade).options(
            joinedload(Grade.enrollment),
            joinedload(Grade.assessment)
        ).filter(Grade.id == grade_id).first()
