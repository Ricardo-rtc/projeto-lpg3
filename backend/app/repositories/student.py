from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models.student import Student
from .base import BaseRepository

class StudentRepository(BaseRepository[Student]):
    def __init__(self, db: Session):
        super().__init__(Student, db)
    
    def get_active_students(self) -> List[Student]:
        return self.db.query(Student).filter(Student.active == True).all()
    
    def get_by_registration(self, registration_number: str) -> Optional[Student]:
        return self.db.query(Student).filter(
            Student.registration_number == registration_number
        ).first()
    
    def get_with_user(self, student_id):
        return self.db.query(Student).options(
            joinedload(Student.user)
        ).filter(Student.id == student_id).first()
