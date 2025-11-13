from sqlalchemy import Column, Numeric, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import uuid

class Grade(Base):
    __tablename__ = "grades"
    __table_args__ = (
        UniqueConstraint('enrollment_id', 'assessment_id', name='uq_grade'),
        CheckConstraint('score >= 0', name='check_score_positive')
    )
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrollment_id = Column(UUID(as_uuid=True), ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    score = Column(Numeric(8, 2), nullable=False)
    recorded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    recorded_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    
    
    enrollment = relationship("Enrollment", back_populates="grades")
    assessment = relationship("Assessment", back_populates="grades")
