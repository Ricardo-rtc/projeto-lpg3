from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.models.grade import Grade
from app.schemas.grade import GradeCreate, GradeUpdate
from app.repositories.grade import GradeRepository
from app.services.enrollment import EnrollmentService

class GradeService:
    def __init__(self, db: Session):
        self.repository = GradeRepository(db)
        self.enrollment_service = EnrollmentService(db)
        self.db = db
    
    def create_grade(self, grade_data: GradeCreate) -> Grade:
        # Verificar se já existe nota para esta avaliação
        existing_grade = self.repository.get_grade(
            grade_data.enrollment_id,
            grade_data.assessment_id
        )
        if existing_grade:
            raise ValueError("Já existe nota para esta avaliação")
        
        grade = Grade(
            enrollment_id=grade_data.enrollment_id,
            assessment_id=grade_data.assessment_id,
            score=grade_data.score,
            recorded_by=grade_data.recorded_by
        )
        created_grade = self.repository.create(grade)
        
        # Recalcular média final
        self.enrollment_service.calculate_final_average(grade_data.enrollment_id)
        
        return created_grade
    
    def update_grade(self, grade_id: uuid.UUID, grade_data: GradeUpdate) -> Optional[Grade]:
        grade = self.repository.get_by_id(grade_id)
        if not grade:
            return None
        
        grade.score = grade_data.score
        if grade_data.recorded_by:
            grade.recorded_by = grade_data.recorded_by
        
        updated_grade = self.repository.update(grade)
        
        # Recalcular média final
        self.enrollment_service.calculate_final_average(grade.enrollment_id)
        
        return updated_grade
    
    def get_by_id(self, grade_id: uuid.UUID) -> Optional[Grade]:
        return self.repository.get_by_id(grade_id)
    
    def get_by_enrollment(self, enrollment_id: uuid.UUID) -> List[Grade]:
        return self.repository.get_by_enrollment(enrollment_id)
    
    def get_by_assessment(self, assessment_id: uuid.UUID) -> List[Grade]:
        return self.repository.get_by_assessment(assessment_id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Grade]:
        return self.repository.get_all(skip, limit)
    
    def delete_grade(self, grade_id: uuid.UUID) -> bool:
        grade = self.repository.get_by_id(grade_id)
        if grade:
            enrollment_id = grade.enrollment_id
            deleted = self.repository.delete(grade_id)
            if deleted:
                # Recalcular média final após deletar
                self.enrollment_service.calculate_final_average(enrollment_id)
            return deleted
        return False
