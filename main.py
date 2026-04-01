from pprint import pp
from financesync.google_api.gmail import get_citi_transactions, get_transactions, unlabel
from financesync.google_api.sheets import write_transactions
from financesync.utils.config import SPREADSHEET_ID

def main():

  transactions = None
  message_ids = None
  
  transactions, message_ids = get_transactions() 

  print("=======================")
  print("Chase")
  print("=======================")

  pp(transactions)

  write_transactions(transactions, SPREADSHEET_ID)

  unlabel(message_ids)

  transactions = None
  message_ids = None
  
  transactions, message_ids = get_citi_transactions() 
  print("=======================")
  print("Citi")
  print("=======================")

  pp(transactions)

  write_transactions(transactions, SPREADSHEET_ID)

  unlabel(message_ids)


if __name__ == "__main__":
  main()