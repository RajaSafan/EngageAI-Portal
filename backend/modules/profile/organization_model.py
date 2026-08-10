"""
backend/modules/profile/organization_model.py

organization_id ab sequential integer hai (1, 2, 3...) — UUID nahi.
"""

import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean
from sqlalchemy.sql import func

from core.database import Base


class OrganizationStatus(str, enum.Enum):
    Active = "Active"
    Inactive = "Inactive"


class Organization(Base):
    __tablename__ = "organizations"

    organization_id = Column(Integer, primary_key=True, autoincrement=True)
    organization_name = Column(String(150), nullable=False)
    business_type = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    business_email = Column(String(255), nullable=True)
    business_phone = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    logo_url = Column(String(255), nullable=True)
    status = Column(Enum(OrganizationStatus), default=OrganizationStatus.Active, nullable=False)
    onboarding_completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)