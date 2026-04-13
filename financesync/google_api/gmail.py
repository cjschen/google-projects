from pprint import pp
from financesync.google_api.credentials import authenticate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from financesync.models.transaction import Transation
from financesync.utils.config import CHASE_AUTOMATION_LABEL, CITI_AUTOMATION_LABEL
from financesync.google_api.email_reader import (
    ChaseEmailParser,
    CitiEmailParser,
    EmailParser,
)


def get_transactions() -> tuple[list[Transation], list[str]]:
    reader = ChaseEmailParser()
    return reader.get_transactions()


def get_citi_transactions() -> tuple[list[Transation], list[str]]:
    reader = CitiEmailParser()
    return reader.get_transactions()


def unlabel(ids: list[str]):
    creds = authenticate()
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        if not ids:
            return

        service.users().messages().batchModify(
            userId="me",
            body={
                "ids": ids,
                "removeLabelIds": [CHASE_AUTOMATION_LABEL, CITI_AUTOMATION_LABEL],
            },
        ).execute()

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


def get_labels():

    creds = authenticate()
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        labels = service.users().labels().list(userId="me").execute()

        return labels
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


def create_filter(bank: EmailParser):
    creds = authenticate()

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)

        # Create a label for the bank
        label_name = bank.get_label()
        
        service.labels().create(
            userId="me", body={"name": label_name}
        ).execute()

        label = (
            service.users()
            .settings()
            .filters()
            .create(userId="me", id=label_name)
            .execute()
        )

        print(f"Name: {label_name}, id: {label['id']}")

        # Create a filter to label incoming emails from the bank
        filter = {
            "criteria": {"from": bank.get_bank_email(), "subject": bank.get_subject()},
            "action": {"addLabelIds": [bank.get_label()]},
        }
        service.users().settings().filters().create(userId="me", body=filter).execute()

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
