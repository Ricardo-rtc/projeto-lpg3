from sqlalchemy.orm import Session, joinedload
from typing import Optional
from app.models.teacher import Teacher
from .base import BaseRepository

class TeacherRepository(BaseRepository[Teacher]):
    def __init__(self, db: Session):
        super().__init__(Teacher, db)
    
    def get_by_employee_number(self, employee_number: str) -> Optional[Teacher]:
        return self.db.query(Teacher).filter(
            Teacher.employee_number == employee_number
        ).first()
    
    def get_with_user(self, teacher_id):
        return self.db.query(Teacher).options(
            joinedload(Teacher.user)
        ).filter(Teacher.id == teacher_id).first()
