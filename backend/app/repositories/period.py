from sqlalchemy.orm import Session
from typing import List
from app.models.period import Period
from .base import BaseRepository

class PeriodRepository(BaseRepository[Period]):
    def __init__(self, db: Session):
        super().__init__(Period, db)
    
    def get_active_periods(self) -> List[Period]:
        return self.db.query(Period).filter(Period.active == True).all()
    
    def get_by_code(self, code: str):
        return self.db.query(Period).filter(Period.code == code).first()
