import base64
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import pytest

from financesync.google_api.email_reader import ChaseEmailParser, CitiEmailParser


class TestEmailParser:

    def get_email(self, bank):

        with open(f"test/test_emails/{bank}.html", "r") as f:
            message = f.read()

        # Get email content and base64 encode it
        chase_email_body = message
        encoded_data = base64.urlsafe_b64encode(
            chase_email_body.encode("UTF8")
        ).decode()

        return encoded_data

    def test_chase_email_parser(self):
        # Mock authenticate to return credentials

        message = {"payload": {"body": {"data": self.get_email("chase")}}}

        # Test
        chase_parser = ChaseEmailParser()
        transaction = chase_parser.get_transaction("id", message)

        assert transaction.str_amount == "$100.00"
        assert transaction.date == datetime(1900, 1, 1, 12, 0)
        assert transaction.merchant == "FOO BAR 00000"

    def test_citi_email_parser(self):
        message = {"payload": {"parts":  [{}, {"body": {"data": self.get_email("citi")}}]}}

        # Test
        citi_parser = CitiEmailParser()
        transaction = citi_parser.get_transaction("id", message)

        assert transaction.str_amount == "$100.00"
        assert transaction.date == datetime(1900, 1, 1, 12, 0)
        assert transaction.merchant == "FOO BAR 00000"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
