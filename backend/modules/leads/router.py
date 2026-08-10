from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import uuid

from core.database import get_db
from modules.auth.service import get_current_user
from modules.leads import schemas, service
from modules.profile.user_model import User

router = APIRouter()


@router.get("/", response_model=List[schemas.LeadOut])
def list_leads(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.get_organization_leads(db, current_user.organization_id)


@router.patch("/{lead_id}/status", response_model=schemas.LeadOut)
def change_lead_status(
    lead_id: uuid.UUID,
    payload: schemas.LeadStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.update_lead_status(db, current_user.organization_id, lead_id, payload.status)