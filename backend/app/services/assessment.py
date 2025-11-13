from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.models.assessment import Assessment
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate
from app.repositories.assessment import AssessmentRepository

class AssessmentService:
    def __init__(self, db: Session):
        self.repository = AssessmentRepository(db)
        self.db = db
    
    def create_assessment(self, assessment_data: AssessmentCreate) -> Assessment:
        assessment = Assessment(
            class_id=assessment_data.class_id,
            name=assessment_data.name,
            description=assessment_data.description,
            date=assessment_data.date,
            weight=assessment_data.weight,
            max_score=assessment_data.max_score
        )
        return self.repository.create(assessment)
    
    def update_assessment(self, assessment_id: uuid.UUID, assessment_data: AssessmentUpdate) -> Optional[Assessment]:
        assessment = self.repository.get_by_id(assessment_id)
        if not assessment:
            return None
        
        if assessment_data.name:
            assessment.name = assessment_data.name
        if assessment_data.description:
            assessment.description = assessment_data.description
        if assessment_data.date:
            assessment.date = assessment_data.date
        if assessment_data.weight:
            assessment.weight = assessment_data.weight
        if assessment_data.max_score:
            assessment.max_score = assessment_data.max_score
        
        return self.repository.update(assessment)
    
    def get_by_id(self, assessment_id: uuid.UUID) -> Optional[Assessment]:
        return self.repository.get_by_id(assessment_id)
    
    def get_by_class(self, class_id: uuid.UUID) -> List[Assessment]:
        return self.repository.get_by_class(class_id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Assessment]:
        return self.repository.get_all(skip, limit)
    
    def delete_assessment(self, assessment_id: uuid.UUID) -> bool:
        return self.repository.delete(assessment_id)
