
from pprint import pp
from google_api.credentials import authenticate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.config import SAMPLE_RANGE_NAME


def write_transactions(transactions: list[list], spreadsheet_id: str): 
  creds = authenticate()
  try:
    service = build("sheets", "v4", credentials=creds)

    body = {"values": transactions}
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=SAMPLE_RANGE_NAME,
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )
    print(f"{(result.get('updates').get('updatedCells'))} cells appended.")

  except HttpError as err:
    print(err)