from datetime import datetime
import json
import re


categories = {}

class Transation:

  def __init__(self, message_id, date, merchant, str_amount, category = None):
    self.message_id = message_id

    self.date = date
    self.merchant = merchant
    self.str_amount = str_amount
    self.set_category()

  def sheet_value(self):
    return [
      datetime.strftime(self.date, '%m-%d-%Y'),
      self.merchant,
      self.str_amount,
      self.category 
    ]
  
  def set_category(self):
    global categories 

    if not categories:
      with open("res/categories.json") as file:
        categories = json.loads(file.read())


    # Ignore ending "SAN FRANCISCOUS" for citi
    merchant = self.merchant.removesuffix("US").strip()
    merchant = merchant.removesuffix("SAN FRANCISCO").strip()

    # Ignore store ID for chains
    self.category = categories.get(re.sub(r'\d+$', '', merchant))

  def __str__(self) -> str:
    return self.sheet_value + ""