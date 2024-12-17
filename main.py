from pprint import pp
from google_api.credentials import authenticate
from google_api.gmail import get_transations, unlabel
from google_api.sheets import write_transactions


def main():

  transactions = None
  message_ids = None
  
  transactions, message_ids = get_transations()

  pp(transactions)

  write_transactions(transactions)

  unlabel(message_ids)



if __name__ == "__main__":
  main()