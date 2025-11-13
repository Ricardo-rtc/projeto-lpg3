from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate
from app.repositories.teacher import TeacherRepository

class TeacherService:
    def __init__(self, db: Session):
        self.repository = TeacherRepository(db)
        self.db = db
    
    def create_teacher(self, teacher_data: TeacherCreate) -> Teacher:
        teacher = Teacher(
            user_id=teacher_data.user_id,
            employee_number=teacher_data.employee_number,
            hire_date=teacher_data.hire_date
        )
        return self.repository.create(teacher)
    
    def update_teacher(self, teacher_id: uuid.UUID, teacher_data: TeacherUpdate) -> Optional[Teacher]:
        teacher = self.repository.get_by_id(teacher_id)
        if not teacher:
            return None
        
        if teacher_data.employee_number:
            teacher.employee_number = teacher_data.employee_number
        if teacher_data.hire_date:
            teacher.hire_date = teacher_data.hire_date
        
        return self.repository.update(teacher)
    
    def get_by_id(self, teacher_id: uuid.UUID) -> Optional[Teacher]:
        return self.repository.get_by_id(teacher_id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Teacher]:
        return self.repository.get_all(skip, limit)
    
    def delete_teacher(self, teacher_id: uuid.UUID) -> bool:
        return self.repository.delete(teacher_id)
