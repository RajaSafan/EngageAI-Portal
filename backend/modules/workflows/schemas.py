from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class MeetingRequest(BaseModel):
    lead_id: uuid.UUID
    department: str                    # Sales / Finance / Support
    preferred_time: datetime
    duration_minutes: int = 30
    notes: str = ""


class MeetingResponse(BaseModel):
    lead_id: uuid.UUID
    assigned_employee_email: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    calendar_event_link: Optional[str] = None
    email_sent: bool
    lead_status: str
    message: str