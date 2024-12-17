from datetime import datetime
import json
import re


categories = {}

class Transation:

  def __init__(self, message_id, str_date, merchant, str_amount, category = None):
    self.message_id = message_id

    self.date = datetime.strptime(str_date.text, '%b %d, %Y at %I:%M %p ET')
    self.merchant = merchant.text
    self.str_amount = str_amount.text
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

    # Ignore store ID for chains

    self.category = categories.get(re.sub(r'\d+$', '', self.merchant))

  def __str__(self) -> str:
    return self.sheet_value + ""