from sqlalchemy import Column, String, Date, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Student(Base):
    __tablename__ = "students"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    registration_number = Column(String, unique=True, index=True)
    enrollment_date = Column(Date)
    birth_date = Column(Date)
    active = Column(Boolean, default=True)
    
    
    user = relationship("User", back_populates="student")
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
