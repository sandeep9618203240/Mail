import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import (
    SCOPES,
    CREDENTIALS_FILE,
    TOKEN_FILE
)


def get_gmail_service():

    credentials = None

    # Check whether token already exists
    if os.path.exists(TOKEN_FILE):

        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    # Refresh expired token
    if credentials and credentials.expired and credentials.refresh_token:

        print("Refreshing Gmail authentication...")

        credentials.refresh(Request())

    # If authentication is not available
    if not credentials or not credentials.valid:

        print("Starting Gmail authentication...")

        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE,
            SCOPES
        )

        credentials = flow.run_local_server(
            port=0
        )

        # Create auth folder
        os.makedirs(
            os.path.dirname(TOKEN_FILE),
            exist_ok=True
        )

        # Save token
        with open(TOKEN_FILE, "w", encoding="utf-8") as token:

            token.write(
                credentials.to_json()
            )

    # Create Gmail API service
    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    return service