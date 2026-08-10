"""
backend/modules/profile/schemas.py

REPLACE the existing file. OrganizationOut mein onboarding_completed add hua.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid


class OrganizationOut(BaseModel):
    organization_id: uuid.UUID
    organization_name: str
    business_type: Optional[str] = None
    website: Optional[str] = None
    business_email: Optional[EmailStr] = None
    business_phone: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    status: str
    onboarding_completed: bool

    class Config:
        from_attributes = True


class OrganizationUpdate(BaseModel):
    organization_name: Optional[str] = None
    business_type: Optional[str] = None
    website: Optional[str] = None
    business_email: Optional[EmailStr] = None
    business_phone: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None


class UserProfileOut(BaseModel):
    user_id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    role: str
    status: str

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None