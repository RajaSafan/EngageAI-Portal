# """
# backend/modules/representatives/schemas.py
# """

# from pydantic import BaseModel, EmailStr
# from typing import Optional
# import uuid


# class RepresentativeCreate(BaseModel):
#     representative_name: str
#     service: Optional[str] = None
#     service_description: Optional[str] = None
#     company_email: EmailStr


# class RepresentativeOut(BaseModel):
#     representative_id: uuid.UUID
#     organization_id: uuid.UUID
#     representative_name: str
#     service: Optional[str] = None
#     service_description: Optional[str] = None
#     company_email: EmailStr
#     invitation_status: Optional[str] = None
#     calendar_connected: bool
#     status: str

#     class Config:
#         from_attributes = True

from datetime import datetime

from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)





class RepresentativeCreate(BaseModel):
    organization_id: UUID | None = None   # optional — router isko current_user se hamesha overwrite karta hai
    representative_name: str
    service: str
    service_description: str
    company_email: EmailStr




class RepresentativeResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )


    representative_id: UUID

    organization_id: UUID

    representative_name: str

    service: str

    service_description: str


    company_email: EmailStr


    invitation_status: str


    calendar_connected: bool


    status: str


    created_at: datetime


    updated_at: datetime