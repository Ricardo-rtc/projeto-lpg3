from sqlalchemy import Column, ForeignKey, Numeric, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import uuid
import enum

class EnrollmentStatus(str, enum.Enum):
    MATRICULADO = "matriculado"
    TRANCADO = "trancado"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"

class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint('student_id', 'class_id', name='uq_enrollment'),)
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    enrolled_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    status = Column(SQLEnum(EnrollmentStatus), default=EnrollmentStatus.MATRICULADO)
    final_average = Column(Numeric(5, 2))
    
    
    student = relationship("Student", back_populates="enrollments")
    class_ = relationship("Class", back_populates="enrollments")
    grades = relationship("Grade", back_populates="enrollment", cascade="all, delete-orphan")
