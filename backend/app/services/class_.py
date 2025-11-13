from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.models.class_ import Class
from app.schemas.class_ import ClassCreate, ClassUpdate
from app.repositories.class_ import ClassRepository

class ClassService:
    def __init__(self, db: Session):
        self.repository = ClassRepository(db)
        self.db = db
    
    def create_class(self, class_data: ClassCreate) -> Class:
        class_obj = Class(
            discipline_id=class_data.discipline_id,
            period_id=class_data.period_id,
            teacher_id=class_data.teacher_id,
            code=class_data.code,
            capacity=class_data.capacity
        )
        return self.repository.create(class_obj)
    
    def update_class(self, class_id: uuid.UUID, class_data: ClassUpdate) -> Optional[Class]:
        class_obj = self.repository.get_by_id(class_id)
        if not class_obj:
            return None
        
        if class_data.teacher_id:
            class_obj.teacher_id = class_data.teacher_id
        if class_data.code:
            class_obj.code = class_data.code
        if class_data.capacity:
            class_obj.capacity = class_data.capacity
        
        return self.repository.update(class_obj)
    
    def get_by_id(self, class_id: uuid.UUID) -> Optional[Class]:
        return self.repository.get_by_id(class_id)
    
    def get_by_period(self, period_id: uuid.UUID) -> List[Class]:
        return self.repository.get_by_period(period_id)
    
    def get_by_teacher(self, teacher_id: uuid.UUID) -> List[Class]:
        return self.repository.get_by_teacher(teacher_id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Class]:
        return self.repository.get_all(skip, limit)
    
    def delete_class(self, class_id: uuid.UUID) -> bool:
        return self.repository.delete(class_id)
