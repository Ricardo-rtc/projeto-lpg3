from sqlalchemy.orm import Session, joinedload
from typing import List
import uuid
from app.models.class_ import Class
from .base import BaseRepository

class ClassRepository(BaseRepository[Class]):
    def __init__(self, db: Session):
        super().__init__(Class, db)
    
    def get_by_period(self, period_id: uuid.UUID) -> List[Class]:
        return self.db.query(Class).filter(Class.period_id == period_id).all()
    
    def get_by_teacher(self, teacher_id: uuid.UUID) -> List[Class]:
        return self.db.query(Class).filter(Class.teacher_id == teacher_id).all()
    
    def get_by_discipline(self, discipline_id: uuid.UUID) -> List[Class]:
        return self.db.query(Class).filter(Class.discipline_id == discipline_id).all()
    
    def get_with_details(self, class_id: uuid.UUID):
        return self.db.query(Class).options(
            joinedload(Class.discipline),
            joinedload(Class.period),
            joinedload(Class.teacher)
        ).filter(Class.id == class_id).first()
