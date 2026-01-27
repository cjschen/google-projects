from pprint import pp
from google_api.gmail import get_citi_transactions, get_transactions, unlabel
from google_api.sheets import write_transactions
from utils.config import SPREADSHEET_ID, JOINT_SPREADSHEET_ID

def main():

  transactions = None
  message_ids = None
  
  transactions, message_ids = get_transactions() 

  print("=======================")
  print("Chase")
  print("=======================")

  pp(transactions)

  write_transactions(transactions, JOINT_SPREADSHEET_ID)

  unlabel(message_ids)

  transactions = None
  message_ids = None
  
  transactions, message_ids = get_citi_transactions() 
  print("=======================")
  print("Citi")
  print("=======================")

  pp(transactions)

  write_transactions(transactions, JOINT_SPREADSHEET_ID)

  unlabel(message_ids)


if __name__ == "__main__":
  main()