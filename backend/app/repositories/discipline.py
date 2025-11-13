from sqlalchemy.orm import Session
from typing import Optional
from app.models.discipline import Discipline
from .base import BaseRepository

class DisciplineRepository(BaseRepository[Discipline]):
    def __init__(self, db: Session):
        super().__init__(Discipline, db)
    
    def get_by_code(self, code: str) -> Optional[Discipline]:
        return self.db.query(Discipline).filter(Discipline.code == code).first()
