from os import getenv
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv()

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = getenv("CLIENT_SECRETS_FILE")

credentials = service_account.Credentials.from_service_account_file(
    CLIENT_SECRETS_FILE
)

SCOPES = ['https://www.googleapis.com/auth/youtube']

scoped_credentials = credentials.with_scopes(SCOPES)
youtube = build('youtube', 'v3', credentials=scoped_credentials)

