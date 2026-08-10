from uuid import UUID


from fastapi import HTTPException


from google_auth_oauthlib.flow import Flow


from google.oauth2.credentials import Credentials


from googleapiclient.discovery import build


from core.config import settings


from core.security import decrypt_token





GOOGLE_SCOPES = [

    "https://www.googleapis.com/auth/calendar",

]







def create_google_flow(
    state: str | None = None,
) -> Flow:


    client_config = {

        "web": {

            "client_id":
                settings.google_client_id,


            "client_secret":
                settings.google_client_secret,


            "auth_uri":
                "https://accounts.google.com/o/oauth2/auth",


            "token_uri":
                "https://oauth2.googleapis.com/token",


            "redirect_uris": [

                settings.google_redirect_uri,

            ],

        }

    }



    flow = Flow.from_client_config(

        client_config=client_config,

        scopes=GOOGLE_SCOPES,

        state=state,

        autogenerate_code_verifier=False,

    )



    flow.redirect_uri = (
        settings.google_redirect_uri
    )



    return flow








def get_representative_or_404(
    db,
    representative_id: UUID,
):

    from modules.representatives.models import Representative



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







def verify_google_calendar_access(
    connection,
):


    if not connection.encrypted_refresh_token:

        raise Exception(
            "Refresh token missing"
        )



    credentials = Credentials(

        token=decrypt_token(

            connection.encrypted_access_token

        ),


        refresh_token=decrypt_token(

            connection.encrypted_refresh_token

        ),


        token_uri=(

            "https://oauth2.googleapis.com/token"

        ),


        client_id=
            settings.google_client_id,


        client_secret=
            settings.google_client_secret,


    )



    service = build(

        "calendar",

        "v3",

        credentials=credentials,

    )



    service.calendarList().list(

        maxResults=1

    ).execute()



    return True