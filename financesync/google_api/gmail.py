from pprint import pp
from financesync.google_api.credentials import authenticate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from financesync.models.transaction import Transation
from financesync.utils.config import AUTOMATION_LABEL, CITI_AUTOMATION_LABEL
from financesync.google_api.email_reader import ChaseEmailParser, CitiEmailParser


def get_transactions() -> tuple[list[Transation], list[str]]:
  reader = ChaseEmailParser()
  return reader.get_transactions()


def get_citi_transactions() -> tuple[list[Transation], list[str]]:
  reader = CitiEmailParser()
  return reader.get_transactions()


def unlabel(ids: list[str]): 
  creds = authenticate()
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    if not ids: 
      return

    service.users().messages().batchModify(userId="me", body = {'ids':ids, 'removeLabelIds':[AUTOMATION_LABEL, CITI_AUTOMATION_LABEL]}).execute()
    
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

def get_labels(): 

  creds = authenticate()
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    
    labels = service.users().labels().list(userId="me").execute()

    return labels
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")