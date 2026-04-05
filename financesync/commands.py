from pprint import pp
from financesync.google_api.gmail import get_citi_transactions, get_transactions, unlabel
from financesync.google_api.sheets import write_transactions
from financesync.utils.config import SPREADSHEET_ID
from financesync.google_api.credentials import authenticate, remove_credentials
import webbrowser

def sync():
  
  chase_transactions, message_ids = get_transactions() 
  
  citi_transactions, message_ids = get_citi_transactions() 

  transactions = chase_transactions + citi_transactions

  transactions.sort(key=lambda x: x.date)

  write_transactions(transactions, SPREADSHEET_ID)

  unlabel(message_ids)

  pp(transactions)

def open():
    webbrowser.open_new_tab(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")

def refresh():
    remove_credentials()
    authenticate()
    
if __name__ == "__main__":
  sync()