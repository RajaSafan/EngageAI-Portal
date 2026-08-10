"""
backend/modules/knowledge/models.py

knowledge_bases table ka SQLAlchemy model. knowledge_base_id aur
organization_id ab sequential integer hain (UUID nahi).
"""

import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func

from core.database import Base


class SourceType(str, enum.Enum):
    Text = "Text"
    PDF = "PDF"
    URL = "URL"


class ProcessingStatus(str, enum.Enum):
    Pending = "Pending"
    Processing = "Processing"
    Completed = "Completed"
    Failed = "Failed"


class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"

    knowledge_base_id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id"), nullable=False)
    source_type = Column(Enum(SourceType), nullable=False)
    source_path = Column(Text, nullable=False)  # file path, raw text, or URL
    processing_status = Column(Enum(ProcessingStatus), default=ProcessingStatus.Pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)