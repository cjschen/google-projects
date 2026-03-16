from abc import ABCMeta, abstractmethod
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


class EmailReader(metaclass=ABCMeta):
    def __init__(self):
        self.service = self._build_service()

    def _build_service(self):
        creds = authenticate()
        return build("gmail", "v1", credentials=creds)

    @abstractmethod
    def get_label(self) -> str:
        pass

    def get_transaction(self, msg_id, msg: dict) -> Transation:
        body = self.decode_body(msg)
        soup = BeautifulSoup(body, "html.parser")

        merchant = self.get_merchant(soup)
        amount = self.get_amount(soup)
        date_obj = self.get_date(soup)

        trans = Transation(msg_id, date_obj, merchant, amount)
        return trans

    def get_transactions(self) -> tuple[list[Transation], list[str]]:
        transactions = []
        ids = []
        try:
            label = self.get_label()
            results = self.service.users().messages().list(userId="me", labelIds=[label]).execute()

            for message in results.get("messages", []):
                try:
                    msg = self.service.users().messages().get(userId="me", id=message["id"]).execute()
                    trans = self.get_transaction(message["id"], msg)
                    transactions.append(trans.sheet_value())
                    ids.append(trans.message_id)
                except Exception as e:
                    print(f"Failed to parse message {message.get('id')}: {e}")

            return list(reversed(transactions)), list(reversed(ids))
        except HttpError as error:
            print(f"An error occurred: {error}")

        return [], []

    @abstractmethod
    def decode_body(self, msg: dict) -> str:
        pass

    @abstractmethod
    def get_merchant(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def get_amount(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def get_date(self, soup: BeautifulSoup) -> datetime:
        pass


class ChaseEmailParser(EmailReader):
    def get_label(self) -> str:
        return AUTOMATION_LABEL

    def decode_body(self, msg: dict) -> str:
        data = msg.get("payload", {}).get("body", {}).get("data")
        if not data:
            return ""
        return base64.urlsafe_b64decode(data).decode("UTF8")

    def get_merchant(self, soup: BeautifulSoup) -> str:
        merchant_el = soup.find("td", string="Merchant")
        return merchant_el.find_next_sibling().text if merchant_el else ""

    def get_amount(self, soup: BeautifulSoup) -> str:
        amount_el = soup.find("td", string="Amount")
        return amount_el.find_next_sibling().text if amount_el else ""

    def get_date(self, soup: BeautifulSoup) -> datetime:
        date_el = soup.find("td", string="Date")
        if date_el:
            date_text = date_el.find_next_sibling().text
            return datetime.strptime(date_text, "%b %d, %Y at %I:%M %p ET")
        return None


class CitiEmailParser(EmailReader):
    def get_label(self) -> str:
        return CITI_AUTOMATION_LABEL

    def decode_body(self, msg: dict) -> str:
        parts = msg.get("payload", {}).get("parts", [])
        if len(parts) > 1:
            data = parts[1].get("body", {}).get("data")
        else:
            data = None

        if not data:
            return ""

        return base64.urlsafe_b64decode(data).decode("UTF8")

    def get_merchant(self, soup: BeautifulSoup) -> str:
        merchant_el = soup.find("td", string="Merchant")
        return merchant_el.find_next_sibling().text if merchant_el else ""

    def get_amount(self, soup: BeautifulSoup) -> str:
        amount_el = soup.find(string=re.compile("Amount:"))
        return amount_el.split(" ")[1] if amount_el else ""

    def get_date(self, soup: BeautifulSoup) -> datetime:
        date_el = soup.find("td", string="Date")
        if date_el:
            date_text = date_el.find_next_sibling().text
            return datetime.strptime(date_text, "%m/%d/%Y")
        return None
