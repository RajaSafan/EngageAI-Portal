"""
backend/modules/auth/schemas.py

REPLACE the existing file. RegisterRequest ab sirf organization_name
(baaki org details onboarding wizard mein) + owner ke fields leta hai.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid


class RegisterRequest(BaseModel):
    # organization ka sirf naam — baaki onboarding wizard Tab 1 mein complete hoga
    organization_name: str
    # owner (user) ke fields
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str


class UserOut(BaseModel):
    user_id: uuid.UUID
    organization_id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    status: str

    class Config:
        from_attributes = True


class RegisterResponse(BaseModel):
    token: str
    user: UserOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    user: UserOut