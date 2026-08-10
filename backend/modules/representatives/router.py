# """
# backend/modules/representatives/router.py
# """

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from typing import List

# from core.database import get_db
# from modules.auth.service import get_current_user
# from modules.representatives import schemas, service
# from modules.profile.user_model import User

# router = APIRouter()


# @router.post("/", response_model=schemas.RepresentativeOut)
# def add_representative(
#     payload: schemas.RepresentativeCreate,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     return service.create_representative(db, current_user.organization_id, payload)


# @router.get("/", response_model=List[schemas.RepresentativeOut])
# def list_representatives(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     return service.get_organization_representatives(db, current_user.organization_id)





from datetime import datetime, timezone
from modules.auth.service import get_current_user
from modules.profile.user_model import User
from uuid import UUID


from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)


from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)


from sqlalchemy import select

from sqlalchemy.orm import Session


from core.database import get_db


from core.security import (
    encrypt_token,
    hash_invitation_token,
)


from modules.representatives.models import (
    Representative,
    CalendarConnection,
)


from modules.representatives.schemas import (
    RepresentativeCreate,
    RepresentativeResponse,
)


from modules.representatives.service import (
    create_representative,
    get_representatives,
    get_representative,
    delete_representative,
)


from modules.representatives.google_calendar import (
    create_google_flow,
    get_representative_or_404,
    verify_google_calendar_access,
)





router = APIRouter(
    prefix="/representatives",
    tags=["Representatives"],
)





# =====================================================
# CREATE REPRESENTATIVE
# =====================================================


@router.post("", response_model=RepresentativeResponse, status_code=status.HTTP_201_CREATED)
def add_representative(
    payload: RepresentativeCreate,
    current_user: User = Depends(get_current_user),   # ADD
    db: Session = Depends(get_db),
):
    payload.organization_id = current_user.organization_id   # payload ka org_id IGNORE karo, apna token wala use karo
    return create_representative(db=db, payload=payload)





# =====================================================
# LIST REPRESENTATIVES
# =====================================================


@router.get("", response_model=list[RepresentativeResponse])
def list_representatives(
    current_user: User = Depends(get_current_user),   # ADD
    db: Session = Depends(get_db),
):
    return get_representatives(db=db, organization_id=current_user.organization_id)   # query param hataya





# =====================================================
# INVITATION PAGE
# =====================================================


@router.get(
    "/invitation/{token}",
    response_class=HTMLResponse,
)
def open_invitation(
    token: str,
    db: Session = Depends(get_db),
):


    token_hash = hash_invitation_token(
        token
    )


    representative = db.scalar(
        select(Representative)
        .where(
            Representative.invitation_token_hash
            ==
            token_hash
        )
    )


    if not representative:

        raise HTTPException(
            status_code=404,
            detail="Invalid invitation link.",
        )



    if (

        representative.invitation_expires_at

        and

        representative.invitation_expires_at
        <
        datetime.now(timezone.utc)

    ):

        representative.invitation_status = (
            "Expired"
        )

        db.commit()


        return """

        <html>

        <body style="
        font-family:Arial;
        text-align:center;
        margin-top:100px;
        ">

        <h2>
        Invitation expired
        </h2>

        </body>

        </html>

        """



    connect_url = (

        f"/representatives/"

        f"{representative.representative_id}"

        f"/google/connect"

    )



    return f"""

    <html>

    <body style="
    font-family:Arial;
    max-width:600px;
    margin:80px auto;
    padding:30px;
    text-align:center;
    border:1px solid #ddd;
    border-radius:12px;
    ">


    <h2>
    Hello {representative.representative_name}
    </h2>


    <p>
    You have been added as a representative.
    </p>


    <h3>
    Service
    </h3>

    <p>
    {representative.service}
    </p>


    <h3>
    Description
    </h3>

    <p>
    {representative.service_description}
    </p>


    <a href="{connect_url}"

    style="
    display:inline-block;
    margin-top:20px;
    padding:14px 30px;
    background:#2563eb;
    color:white;
    text-decoration:none;
    border-radius:8px;
    ">

    Connect Google Calendar

    </a>


    </body>

    </html>

    """







# =====================================================
# GOOGLE CONNECT
# =====================================================


@router.get(
    "/{representative_id}/google/connect",
)
def connect_google_calendar(
    representative_id: UUID,
    db: Session = Depends(get_db),
):


    representative = get_representative_or_404(
        db=db,
        representative_id=representative_id,
    )


    flow = create_google_flow(
        state=str(
            representative.representative_id
        ),
    )


    authorization_url, _ = (
        flow.authorization_url(
            access_type="offline",
            prompt="consent",
            include_granted_scopes="true",
            login_hint=
                representative.company_email,
        )
    )


    return RedirectResponse(
        authorization_url,
        status_code=302,
    )







# =====================================================
# GOOGLE CALLBACK
# =====================================================


@router.get(
    "/google/callback",
    response_class=HTMLResponse,
)
def google_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):


    try:

        representative_id = UUID(
            state
        )

    except ValueError:


        raise HTTPException(
            status_code=400,
            detail="Invalid OAuth state.",
        )



    representative = get_representative_or_404(
        db=db,
        representative_id=representative_id,
    )



    flow = create_google_flow(
        state=state,
    )



    try:

        flow.fetch_token(
            code=code,
        )

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=f"Google OAuth failed: {error}",
        )



    credentials = flow.credentials



    if not credentials.token:

        raise HTTPException(
            status_code=400,
            detail="Google access token missing.",
        )



    connection = db.scalar(
        select(CalendarConnection)
        .where(
            CalendarConnection.representative_id
            ==
            representative_id
        )
    )



    if connection is None:


        connection = CalendarConnection(

            representative_id=
                representative_id

        )


        db.add(
            connection
        )



    connection.encrypted_access_token = (
        encrypt_token(
            credentials.token
        )
    )



    if credentials.refresh_token:

        connection.encrypted_refresh_token = (
            encrypt_token(
                credentials.refresh_token
            )
        )



    if not connection.encrypted_refresh_token:

        raise HTTPException(
            status_code=400,
            detail=(
                "No refresh token received. "
                "Remove Google access and reconnect."
            ),
        )



    connection.token_expiry = (
        credentials.expiry
    )


    connection.google_calendar_id = (
        "primary"
    )


    connection.connection_status = (
        "Connected"
    )


    connection.last_verified_at = (
        datetime.now(timezone.utc)
    )



    representative.calendar_connected = True


    representative.invitation_status = (
        "Accepted"
    )



    db.commit()



    return """

    <html>

    <body style="
    font-family:Arial;
    text-align:center;
    margin-top:100px;
    ">


    <h2 style="color:green">

    Calendar accessed successfully.

    </h2>


    <p>
    Your Google Calendar is now connected.
    </p>


    <p>
    You can close this page.
    </p>


    </body>

    </html>

    """







# =====================================================
# CALENDAR STATUS CHECK
# =====================================================


@router.get(
    "/{representative_id}/calendar/check",
)
def check_calendar_status(
    representative_id: UUID,
    db: Session = Depends(get_db),
):


    representative = get_representative(
        db=db,
        representative_id=representative_id,
    )



    connection = db.scalar(
        select(CalendarConnection)
        .where(
            CalendarConnection.representative_id
            ==
            representative_id
        )
    )



    if not connection:

        return {

            "representative_id":
                str(representative_id),

            "calendar_connected":
                False,

            "connection_status":
                "Not Connected",
        }





    try:


        verify_google_calendar_access(
            connection
        )


        connection.connection_status = (
            "Connected"
        )


        representative.calendar_connected = True


        connection.last_verified_at = (
            datetime.now(timezone.utc)
        )



    except Exception as error:


        print(
            f"Google calendar revoked: {error}",
            flush=True,
        )


        connection.connection_status = (
            "Revoked"
        )


        representative.calendar_connected = False



    db.commit()



    return {

        "representative_id":
            str(representative_id),


        "calendar_connected":
            representative.calendar_connected,


        "connection_status":
            connection.connection_status,

    }





# =====================================================
# GET ONE
# =====================================================

@router.get("/{representative_id}", response_model=RepresentativeResponse)
def retrieve_representative(
    representative_id: UUID,
    current_user: User = Depends(get_current_user),   # ADD
    db: Session = Depends(get_db),
):
    rep = get_representative(db=db, representative_id=representative_id)
    if rep.organization_id != current_user.organization_id:   # ADD
        raise HTTPException(status_code=403, detail="Not your organization's representative")
    return rep






# =====================================================
# DELETE
# =====================================================



@router.delete("/{representative_id}", status_code=204)
def remove_representative(
    representative_id: UUID,
    current_user: User = Depends(get_current_user),   # ADD
    db: Session = Depends(get_db),
):
    rep = get_representative(db=db, representative_id=representative_id)
    if rep.organization_id != current_user.organization_id:   # ADD
        raise HTTPException(status_code=403, detail="Not your organization's representative")
    delete_representative(db=db, representative_id=representative_id)
    return None