from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_query_email(subject, message, recipient_list):
    try:
        if not subject:
            raise ValidationError("The email subject cannot be empty.")
        if not message:
            raise ValidationError("The email message cannot be empty.")
        if not recipient_list or not all(recipient_list):
            raise ValidationError(
                "The recipient list must contain at least one valid email address.")

        sender_email = settings.MAILJET_SENDER_EMAIL
        if not sender_email:
            raise ValidationError(
                "The sender email is not configured correctly.")

        send_mail(
            subject,
            message,
            sender_email,
            recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email successfully sent to {', '.join(recipient_list)}")
    except ValidationError as e:
        logger.error(f"Validation error while sending email: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred while sending email: {e}")
        raise
