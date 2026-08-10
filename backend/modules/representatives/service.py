# """
# backend/modules/representatives/service.py

# NOTE: Ye sirf representative ka RECORD create/list karta hai (onboarding ke
# liye kaafi hai). Actual invitation email bhejna aur calendar OAuth connect
# karna (invitation_token_hash, calendar_connected=True karna) alag feature
# hai — jo workflows/calendar module banayega wo isi table ko update karega.
# """

# from sqlalchemy.orm import Session

# from modules.representatives.models import Representative


# def create_representative(db: Session, organization_id, data):
#     rep = Representative(
#         organization_id=organization_id,
#         representative_name=data.representative_name,
#         service=data.service,
#         service_description=data.service_description,
#         company_email=data.company_email,
#         invitation_status="Pending",
#     )
#     db.add(rep)
#     db.commit()
#     db.refresh(rep)
#     return rep


# def get_organization_representatives(db: Session, organization_id):
#     return (
#         db.query(Representative)
#         .filter(Representative.organization_id == organization_id)
#         .order_by(Representative.created_at.desc())
#         .all()
#     )




from datetime import (
    datetime,
    timedelta,
    timezone,
)

from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from core.config import settings


from core.security import (
    create_invitation_token,
)


from modules.representatives.email_service import (
    send_representative_invitation,
)


from modules.representatives.models import (
    Representative,
)


from modules.representatives.schemas import (
    RepresentativeCreate,
)





def create_representative(
    db: Session,
    payload: RepresentativeCreate,
) -> Representative:


    raw_token, token_hash = (
        create_invitation_token()
    )



    representative = Representative(

        organization_id=
            payload.organization_id,


        representative_name=
            payload.representative_name.strip(),


        service=
            payload.service.strip(),


        service_description=
            payload.service_description.strip(),


        company_email=
            str(payload.company_email)
            .strip()
            .lower(),


        invitation_token_hash=
            token_hash,


        invitation_expires_at=
            (
                datetime.now(timezone.utc)
                +
                timedelta(hours=24)
            ),


        invitation_status=
            "Pending",

    )



    db.add(
        representative
    )


    try:

        db.commit()

        db.refresh(
            representative
        )


    except IntegrityError:

        db.rollback()


        raise HTTPException(
            status_code=409,
            detail=(
                "A representative with this "
                "email already exists in this organization."
            ),
        )



    invitation_url = (

        f"{settings.backend_url.rstrip('/')}"

        f"/representatives/invitation/"

        f"{raw_token}"

    )



    try:


        send_representative_invitation(

            representative_name=
                representative.representative_name,


            company_email=
                representative.company_email,


            service=
                representative.service,


            invitation_url=
                invitation_url,

        )


        representative.invitation_status = (
            "Sent"
        )



    except Exception as error:


        representative.invitation_status = (
            "Email Failed"
        )


        print(

            f"Invitation email failed: "
            f"{type(error).__name__}: {error}",

            flush=True,

        )



    db.commit()

    db.refresh(
        representative
    )


    return representative




def get_representatives(db: Session, organization_id: UUID) -> list[Representative]:
    statement = (
        select(Representative)
        .where(Representative.organization_id == organization_id)
        .order_by(Representative.created_at.desc())
    )
    return list(db.scalars(statement).all())





def get_representative(
    db: Session,
    representative_id: UUID,
) -> Representative:


    representative = db.get(

        Representative,

        representative_id,

    )


    if not representative:

        raise HTTPException(

            status_code=404,

            detail="Representative not found.",

        )


    return representative








def delete_representative(
    db: Session,
    representative_id: UUID,
) -> None:


    representative = get_representative(

        db=db,

        representative_id=representative_id,

    )


    db.delete(
        representative
    )


    db.commit()