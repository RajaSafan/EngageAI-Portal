from pydantic import BaseModel, EmailStr


class EmployeeOut(BaseModel):
    user_id: int
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