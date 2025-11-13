from sqlalchemy.orm import Session
from decimal import Decimal
from typing import List, Optional
import uuid
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.class_ import Class
from app.models.grade import Grade
from app.models.assessment import Assessment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate
from app.repositories.enrollment import EnrollmentRepository
from sqlalchemy import func

class EnrollmentService:
    def __init__(self, db: Session):
        self.repository = EnrollmentRepository(db)
        self.db = db
    
    def enroll_student(self, enrollment_data: EnrollmentCreate) -> Enrollment:
        # Verificar se já existe matrícula
        if self.repository.exists_enrollment(
            enrollment_data.student_id, 
            enrollment_data.class_id
        ):
            raise ValueError("Aluno já está matriculado nesta turma")
        
        # Verificar capacidade
        current_count = self.db.query(func.count(Enrollment.id))\
            .filter(Enrollment.class_id == enrollment_data.class_id).scalar()
        
        class_obj = self.db.query(Class).filter(
            Class.id == enrollment_data.class_id
        ).first()
        
        if class_obj and class_obj.capacity and current_count >= class_obj.capacity:
            raise ValueError("Turma está com capacidade máxima")
        
        enrollment = Enrollment(
            student_id=enrollment_data.student_id,
            class_id=enrollment_data.class_id,
            status=enrollment_data.status
        )
        return self.repository.create(enrollment)
    
    def update_enrollment(self, enrollment_id: uuid.UUID, enrollment_data: EnrollmentUpdate) -> Optional[Enrollment]:
        enrollment = self.repository.get_by_id(enrollment_id)
        if not enrollment:
            return None
        
        if enrollment_data.status:
            enrollment.status = enrollment_data.status
        if enrollment_data.final_average is not None:
            enrollment.final_average = enrollment_data.final_average
        
        return self.repository.update(enrollment)
    
    def calculate_final_average(self, enrollment_id: uuid.UUID) -> Decimal:
        grades = self.db.query(Grade).join(Assessment)\
            .filter(Grade.enrollment_id == enrollment_id).all()
        
        if not grades:
            return Decimal(0)
        
        total_weight = sum(Decimal(str(g.assessment.weight)) for g in grades)
        weighted_sum = sum(
            (Decimal(str(g.score)) / Decimal(str(g.assessment.max_score))) * 
            Decimal("100") * Decimal(str(g.assessment.weight))
            for g in grades
        )
        
        final_avg = Decimal(weighted_sum / total_weight if total_weight > 0 else 0)
        
        # Atualizar a média final na matrícula
        enrollment = self.repository.get_by_id(enrollment_id)
        if enrollment:
            enrollment.final_average = final_avg
            self.repository.update(enrollment)
        
        return final_avg
    
    def get_by_id(self, enrollment_id: uuid.UUID) -> Optional[Enrollment]:
        return self.repository.get_by_id(enrollment_id)
    
    def get_by_student(self, student_id: uuid.UUID) -> List[Enrollment]:
        return self.repository.get_by_student(student_id)
    
    def get_by_class(self, class_id: uuid.UUID) -> List[Enrollment]:
        return self.repository.get_by_class(class_id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Enrollment]:
        return self.repository.get_all(skip, limit)
    
    def delete_enrollment(self, enrollment_id: uuid.UUID) -> bool:
        return self.repository.delete(enrollment_id)
