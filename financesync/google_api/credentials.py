import os
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from financesync.utils.config import SCOPES

creds = None

def remove_credentials():
  global creds
  creds = None

  if os.path.exists("data/token.json"):
    os.remove("data/token.json")

def authenticate(force_auth = False) -> None:
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  global creds

  if creds and not force_auth: 
    return creds

  if os.path.exists("data/token.json"):
    try: 
      creds = Credentials.from_authorized_user_file("data/token.json", SCOPES)
    except RefreshError: 
      pass

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "secrets/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("data/token.json", "w") as token:
      token.write(creds.to_json())

  return creds
