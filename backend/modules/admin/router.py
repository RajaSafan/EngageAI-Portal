from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from modules.auth.service import get_current_user
from modules.admin import schemas, service
from modules.profile.user_model import User

router = APIRouter()


@router.post("/employees", response_model=schemas.EmployeeOut)
def create_employee(
    payload: schemas.CreateEmployeeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service.ensure_owner(current_user)
    return service.create_employee(db, current_user.organization_id, payload)


@router.get("/users", response_model=List[schemas.EmployeeOut])
def list_employees(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service.ensure_owner(current_user)
    return service.get_employees(db, current_user.organization_id)


@router.patch("/users/{user_id}/status", response_model=schemas.EmployeeOut)
def toggle_status(
    user_id: str,
    payload: schemas.StatusUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service.ensure_owner(current_user)
    return service.update_employee_status(db, current_user.organization_id, user_id, payload.status)