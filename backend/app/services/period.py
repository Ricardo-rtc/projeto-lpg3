from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.models.period import Period
from app.schemas.period import PeriodCreate, PeriodUpdate
from app.repositories.period import PeriodRepository

class PeriodService:
    def __init__(self, db: Session):
        self.repository = PeriodRepository(db)
        self.db = db
    
    def create_period(self, period_data: PeriodCreate) -> Period:
        period = Period(
            code=period_data.code,
            name=period_data.name,
            start_date=period_data.start_date,
            end_date=period_data.end_date,
            active=period_data.active
        )
        return self.repository.create(period)
    
    def update_period(self, period_id: uuid.UUID, period_data: PeriodUpdate) -> Optional[Period]:
        period = self.repository.get_by_id(period_id)
        if not period:
            return None
        
        if period_data.name:
            period.name = period_data.name
        if period_data.start_date:
            period.start_date = period_data.start_date
        if period_data.end_date:
            period.end_date = period_data.end_date
        if period_data.active is not None:
            period.active = period_data.active
        
        return self.repository.update(period)
    
    def get_by_id(self, period_id: uuid.UUID) -> Optional[Period]:
        return self.repository.get_by_id(period_id)
    
    def get_active_periods(self) -> List[Period]:
        return self.repository.get_active_periods()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Period]:
        return self.repository.get_all(skip, limit)
    
    def delete_period(self, period_id: uuid.UUID) -> bool:
        return self.repository.delete(period_id)
