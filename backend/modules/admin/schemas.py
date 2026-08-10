from pydantic import BaseModel, EmailStr
import uuid


class EmployeeOut(BaseModel):
    user_id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    status: str

    class Config:
        from_attributes = True


class StatusUpdateRequest(BaseModel):
    status: str


class CreateEmployeeRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str
    role: str   # Sales / Finance / Support (Owner allowed nahi is endpoint se)