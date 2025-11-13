from sqlalchemy import Column, String, Date, Numeric, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import uuid

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    date = Column(Date)
    weight = Column(Numeric(5, 2), default=1.0, nullable=False)
    max_score = Column(Numeric(8, 2), default=100)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    
    
    class_ = relationship("Class", back_populates="assessments")
    grades = relationship("Grade", back_populates="assessment", cascade="all, delete-orphan")
