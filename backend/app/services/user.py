from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user import UserRepository
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role
        )
        return self.repository.create(user)
    
    def update_user(self, user_id: uuid.UUID, user_data: UserUpdate) -> Optional[User]:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        
        if user_data.email:
            user.email = user_data.email
        if user_data.full_name:
            user.full_name = user_data.full_name
        if user_data.password:
            user.password = get_password_hash(user_data.password)
        
        return self.repository.update(user)
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.repository.get_by_username(username)
        if user and verify_password(password, user.password):
            return user
        return None
    
    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self.repository.get_by_id(user_id)
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.repository.get_by_username(username)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.repository.get_all(skip, limit)
    
    def delete_user(self, user_id: uuid.UUID) -> bool:
        return self.repository.delete(user_id)
