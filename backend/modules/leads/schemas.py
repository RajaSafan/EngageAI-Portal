from pydantic import BaseModel
from typing import Optional
import uuid

class LeadOut(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    visitor_name: Optional[str] = None
    visitor_email: Optional[str] = None
    status: str

    class Config:
        from_attributes = True


class LeadStatusUpdate(BaseModel):
    status: str