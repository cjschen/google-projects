import webbrowser
from utils.config import SPREADSHEET_ID

# This doesn't work currently
if __name__ == "__main__":
  webbrowser.open_new_tab(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")