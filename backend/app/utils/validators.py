import uuid
from typing import Optional

def validate_uuid(uuid_string: str) -> Optional[uuid.UUID]:
    """Valida se uma string é um UUID válido"""
    try:
        return uuid.UUID(uuid_string)
    except (ValueError, AttributeError):
        return None
