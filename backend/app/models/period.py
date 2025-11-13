from sqlalchemy import Column, String, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Period(Base):
    __tablename__ = "periods"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False)
    name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    active = Column(Boolean, default=True)
    
    
    classes = relationship("Class", back_populates="period")
