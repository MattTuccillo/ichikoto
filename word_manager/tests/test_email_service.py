from django.core.exceptions import ValidationError
from django.test import TestCase
from django.conf import settings
from unittest.mock import patch
from ..services.email_service import send_query_email


class SendQueryEmailTest(TestCase):

    # successful send
    @patch('word_manager.services.email_service.send_mail')
    def test_send_query_email_success(self, mock_send_mail):
        subject = "Test Subject"
        message = "Test message"
        recipient_list = ["test@example.com"]

        send_query_email(subject, message, recipient_list)

        mock_send_mail.assert_called_once_with(
            subject,
            message,
            settings.MAILJET_SENDER_EMAIL,
            recipient_list,
            fail_silently=False,
        )

    # invalid subject
    def test_send_query_email_with_invalid_subject(self):
        subject = ""
        message = "Test message"
        recipient_list = ["test@example.com"]

        with self.assertRaises(ValidationError):
            send_query_email(subject, message, recipient_list)

    # invalid message
    def test_send_query_email_with_invalid_message(self):
        subject = "Test Subject"
        message = ""
        recipient_list = ["test@example.com"]

        with self.assertRaises(ValidationError):
            send_query_email(subject, message, recipient_list)

    # invalid recipients list
    def test_send_query_email_with_invalid_recipient(self):
        subject = "Test Subject"
        message = "Test message"
        recipient_list = []

        with self.assertRaises(ValidationError):
            send_query_email(subject, message, recipient_list)
