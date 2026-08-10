"""
backend/modules/profile/user_model.py

users table ka SQLAlchemy model. user_id aur organization_id ab sequential
integer hain (UUID nahi). role aur status dono ENUM hain.
"""

import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class UserRole(str, enum.Enum):
    Owner = "Owner"
    Sales = "Sales"
    Finance = "Finance"
    Support = "Support"


class UserStatus(str, enum.Enum):
    Active = "Active"
    Inactive = "Inactive"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.Owner, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.Active, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    organization = relationship("Organization", backref="users")