from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 100

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    skip: int
    limit: int
    
    class Config:
        from_attributes = True

class Paginator:
    @staticmethod
    def paginate(items: List[T], total: int, skip: int, limit: int) -> PaginatedResponse[T]:
        return PaginatedResponse(
            items=items,
            total=total,
            skip=skip,
            limit=limit
        )
