from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from app.core.database import Base
from datetime import datetime
import uuid

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schema_name = Column(String, nullable=False)
    table_name = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    record_id = Column(String)
    changed_data = Column(JSONB)
    changed_by = Column(String)
    changed_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
