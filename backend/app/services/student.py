from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.repositories.student import StudentRepository

class StudentService:
    def __init__(self, db: Session):
        self.repository = StudentRepository(db)
        self.db = db
    
    def create_student(self, student_data: StudentCreate) -> Student:
        student = Student(
            user_id=student_data.user_id,
            registration_number=student_data.registration_number,
            enrollment_date=student_data.enrollment_date,
            birth_date=student_data.birth_date,
            active=student_data.active
        )
        return self.repository.create(student)
    
    def update_student(self, student_id: uuid.UUID, student_data: StudentUpdate) -> Optional[Student]:
        student = self.repository.get_by_id(student_id)
        if not student:
            return None
        
        if student_data.registration_number:
            student.registration_number = student_data.registration_number
        if student_data.birth_date:
            student.birth_date = student_data.birth_date
        if student_data.active is not None:
            student.active = student_data.active
        
        return self.repository.update(student)
    
    def get_by_id(self, student_id: uuid.UUID) -> Optional[Student]:
        return self.repository.get_by_id(student_id)
    
    def get_active_students(self) -> List[Student]:
        return self.repository.get_active_students()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Student]:
        return self.repository.get_all(skip, limit)
    
    def delete_student(self, student_id: uuid.UUID) -> bool:
        return self.repository.delete(student_id)
