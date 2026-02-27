from pprint import pp
from datetime import datetime
from google_api.credentials import authenticate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from bs4 import BeautifulSoup
from models.transaction import Transation
from utils.config import AUTOMATION_LABEL, CITI_AUTOMATION_LABEL
import re

def get_transactions() -> tuple[list[Transation], list[str]]: 
  creds = authenticate()
  transactions = []
  ids = []
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", labelIds=[AUTOMATION_LABEL]).execute()
    
    for message in results.get("messages", []):
      msg = service.users().messages().get(userId="me", id=message["id"]).execute()
      body = base64.urlsafe_b64decode(msg["payload"]["body"]["data"]).decode('UTF8')
      soup = BeautifulSoup(body, 'html.parser')
      merchant = soup.find('td', string = "Merchant").find_next_sibling().text
      amount = soup.find('td', string = "Amount").find_next_sibling().text
      date = soup.find('td', string = "Date").find_next_sibling()
      datetime_obj = datetime.strptime(date.text, '%b %d, %Y at %I:%M %p ET')
      trans = Transation(message["id"], datetime_obj, merchant, amount)
      transactions.append(trans.sheet_value())
      ids.append(trans.message_id)
    
    return list(reversed(transactions)), list(reversed(ids))
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

  return [], []

def get_citi_transactions() -> tuple[list[Transation], list[str]]:
  
  creds = authenticate()
  transactions = []
  ids = []
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", labelIds=[CITI_AUTOMATION_LABEL]).execute()
    for message in results.get("messages", []):
      msg = service.users().messages().get(userId="me", id=message["id"]).execute()
      # if msg["payload"]["parts"][1]["body"]["size"] == 0: 
      #   pass
      body = base64.urlsafe_b64decode(msg["payload"]["parts"][1]["body"]["data"]).decode('UTF8')
      soup = BeautifulSoup(body, 'html.parser')
      merchant = soup.find('td', string = "Merchant").find_next_sibling().text
      date = soup.find('td', string = "Date").find_next_sibling()
      amount = soup.find(string=re.compile("Amount:")).split(' ')[1]
      datetime_obj = datetime.strptime(date.text, '%m/%d/%Y')
      trans = Transation(message["id"], datetime_obj, merchant, amount)
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