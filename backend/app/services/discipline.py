from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.models.discipline import Discipline
from app.schemas.discipline import DisciplineCreate, DisciplineUpdate
from app.repositories.discipline import DisciplineRepository

class DisciplineService:
    def __init__(self, db: Session):
        self.repository = DisciplineRepository(db)
        self.db = db
    
    def create_discipline(self, discipline_data: DisciplineCreate) -> Discipline:
        discipline = Discipline(
            code=discipline_data.code,
            name=discipline_data.name,
            description=discipline_data.description,
            credits=discipline_data.credits
        )
        return self.repository.create(discipline)
    
    def update_discipline(self, discipline_id: uuid.UUID, discipline_data: DisciplineUpdate) -> Optional[Discipline]:
        discipline = self.repository.get_by_id(discipline_id)
        if not discipline:
            return None
        
        if discipline_data.name:
            discipline.name = discipline_data.name
        if discipline_data.description:
            discipline.description = discipline_data.description
        if discipline_data.credits:
            discipline.credits = discipline_data.credits
        
        return self.repository.update(discipline)
    
    def get_by_id(self, discipline_id: uuid.UUID) -> Optional[Discipline]:
        return self.repository.get_by_id(discipline_id)
    
    def get_by_code(self, code: str) -> Optional[Discipline]:
        return self.repository.get_by_code(code)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Discipline]:
        return self.repository.get_all(skip, limit)
    
    def delete_discipline(self, discipline_id: uuid.UUID) -> bool:
        return self.repository.delete(discipline_id)
