from pprint import pp
from google_api.credentials import authenticate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from bs4 import BeautifulSoup
from models.transaction import Transation
from utils.config import AUTOMATION_LABEL

def get_transations() -> tuple[list[Transation], list[str]]: 
  creds = authenticate()
  transactions = []
  ids = []
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", labelIds=[AUTOMATION_LABEL]).execute()
    # results = service.users().labels().list(userId="me").execute()
    for message in results.get("messages", []):
      msg = service.users().messages().get(userId="me", id=message["id"]).execute()
      body = base64.urlsafe_b64decode(msg["payload"]["body"]["data"]).decode('UTF8')
      soup = BeautifulSoup(body, 'html.parser')
      merchant = soup.find('td', string = "Merchant").find_next_sibling()
      amount = soup.find('td', string = "Amount").find_next_sibling()
      date = soup.find('td', string = "Date").find_next_sibling()
      trans = Transation(message["id"], date, merchant, amount)
      transactions.append(trans.sheet_value())
      ids.append(trans.message_id)
    
    return list(reversed(transactions)), list(reversed(ids))
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

  return [], []


def unlabel(ids: list[str]): 
  creds = authenticate()
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    if not ids: 
      return

    service.users().messages().batchModify(userId="me", body = {'ids':ids, 'removeLabelIds':[AUTOMATION_LABEL]}).execute()
    
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")