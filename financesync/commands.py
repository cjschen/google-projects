from pprint import pp
from financesync.google_api.email_reader import ChaseEmailParser, CitiEmailParser
from financesync.google_api.gmail import create_filter, get_citi_transactions, get_transactions, unlabel
from financesync.google_api.sheets import write_transactions
from financesync.utils.config import SPREADSHEET_ID
from financesync.google_api.credentials import authenticate, remove_credentials
import webbrowser

def sync():
  
  chase_transactions, chase_message_ids = get_transactions() 
  
  citi_transactions, citi_message_ids = get_citi_transactions() 

  transactions = chase_transactions + citi_transactions

  message_ids = citi_message_ids + chase_message_ids

  transactions.sort(key=lambda x: x.date)

  transaction_transformed = [t.sheet_value() for t in transactions]

  write_transactions(transaction_transformed, SPREADSHEET_ID)

  unlabel(message_ids)

  pp(transaction_transformed)

def open():
    webbrowser.open_new_tab(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")

def refresh():
    remove_credentials()
    authenticate()

def create_filters():
    create_filter(ChaseEmailParser())
    create_filter(CitiEmailParser())
    
if __name__ == "__main__":
  sync()