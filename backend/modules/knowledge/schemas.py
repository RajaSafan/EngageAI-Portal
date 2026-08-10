from pydantic import BaseModel
from typing import Optional
import uuid


class KnowledgeBaseOut(BaseModel):
    knowledge_base_id: uuid.UUID
    organization_id: uuid.UUID
    source_type: str
    source_path: str
    processing_status: str

    class Config:
        from_attributes = True


class TextSourceCreate(BaseModel):
    """Jab source_type = Text ho — raw text seedha bheja jata hai."""
    content: str


class UrlSourceCreate(BaseModel):
    """Jab source_type = URL ho."""
    url: str