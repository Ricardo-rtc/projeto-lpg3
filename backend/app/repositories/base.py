from sqlalchemy.orm import Session
from typing import List, Optional, Type, TypeVar, Generic, Dict, Any
import uuid

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db
    
    def get_by_id(self, id: uuid.UUID) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100, filters: Dict[str, Any] = None) -> List[T]:
        query = self.db.query(self.model)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
        return query.offset(skip).limit(limit).all()
    
    def count(self, filters: Dict[str, Any] = None) -> int:
        query = self.db.query(self.model)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
        return query.count()
    
    def create(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj: T) -> T:
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, id: uuid.UUID) -> bool:
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
    
    def exists(self, id: uuid.UUID) -> bool:
        return self.db.query(self.model).filter(self.model.id == id).first() is not None
