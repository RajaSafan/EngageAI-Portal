"""
backend/modules/profile/organization_model.py

REPLACE the existing file with this. Changes:
- onboarding_completed column add hua
- business_type, website, business_email, business_phone, country ab nullable
  hain (signup ke waqt nahi bharte, onboarding wizard mein complete hote hain)
"""

import uuid
import enum
from sqlalchemy import Column, String, Text, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.database import Base


class OrganizationStatus(str, enum.Enum):
    Active = "Active"
    Inactive = "Inactive"


class Organization(Base):
    __tablename__ = "organizations"

    organization_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
