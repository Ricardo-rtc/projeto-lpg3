from sqlalchemy.orm import Session, joinedload
from typing import List
import uuid
from app.models.enrollment import Enrollment, EnrollmentStatus
from .base import BaseRepository

class EnrollmentRepository(BaseRepository[Enrollment]):
    def __init__(self, db: Session):
        super().__init__(Enrollment, db)
    
    def get_by_student(self, student_id: uuid.UUID) -> List[Enrollment]:
        return self.db.query(Enrollment).filter(
            Enrollment.student_id == student_id
        ).all()
    
    def get_by_class(self, class_id: uuid.UUID) -> List[Enrollment]:
        return self.db.query(Enrollment).filter(
            Enrollment.class_id == class_id
        ).all()
    
    def get_by_status(self, status: EnrollmentStatus) -> List[Enrollment]:
        return self.db.query(Enrollment).filter(
            Enrollment.status == status
        ).all()
    
    def get_with_details(self, enrollment_id: uuid.UUID):
        return self.db.query(Enrollment).options(
            joinedload(Enrollment.student),
            joinedload(Enrollment.class_)
        ).filter(Enrollment.id == enrollment_id).first()
    
    def exists_enrollment(self, student_id: uuid.UUID, class_id: uuid.UUID) -> bool:
        return self.db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.class_id == class_id
        ).first() is not None
