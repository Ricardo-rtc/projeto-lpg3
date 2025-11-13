from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum
from app.core.database import Base
from .user import UserRole

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True)
    role = Column(SQLEnum(UserRole), nullable=False)
    resource = Column(String, nullable=False)
    can_read = Column(Boolean, default=False)
    can_write = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
