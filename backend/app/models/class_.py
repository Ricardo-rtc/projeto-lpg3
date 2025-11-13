from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import uuid

class Class(Base):
    __tablename__ = "classes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    discipline_id = Column(UUID(as_uuid=True), ForeignKey("disciplines.id", ondelete="RESTRICT"), nullable=False)
    period_id = Column(UUID(as_uuid=True), ForeignKey("periods.id", ondelete="RESTRICT"), nullable=False, index=True)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id", ondelete="SET NULL"))
    code = Column(String)
    capacity = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    
    
    discipline = relationship("Discipline", back_populates="classes")
    period = relationship("Period", back_populates="classes")
    teacher = relationship("Teacher", back_populates="classes")
    enrollments = relationship("Enrollment", back_populates="class_", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="class_", cascade="all, delete-orphan")
