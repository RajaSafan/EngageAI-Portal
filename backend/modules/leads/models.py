"""
backend/modules/leads/models.py

leads table ka SQLAlchemy model. id aur organization_id ab sequential
integer hain (UUID nahi).
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from core.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(
        Integer,
        ForeignKey("organizations.organization_id"),
        nullable=False,
    )
    visitor_name = Column(String(150), nullable=True)
    visitor_email = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default="New")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )