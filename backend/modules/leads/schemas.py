from pydantic import BaseModel
from typing import Optional

class LeadOut(BaseModel):
    id: int
    organization_id: int
    visitor_name: Optional[str] = None
    visitor_email: Optional[str] = None
    status: str

    class Config:
        from_attributes = True


class LeadStatusUpdate(BaseModel):
    status: str