from django.core.management.base import BaseCommand
from django.conf import settings
from ...services.email_service import send_query_email
from ...services.gpt_service import send_prompt
from ...services.word_service import store_word
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends the daily word email'

    def handle(self, *args, **kwargs):
        try:
            logger.info("Attempting to fetch the daily word...")
            word_info = send_prompt()
            word_info = word_info.choices[0].message.content

            if word_info:
                logger.info(f"Word fetched: {word_info}")

                logger.info("Storing the word in the database...")
                store_word(word_info)

                message = word_info
                subject = "Word of the Day"
                recipient_list = [settings.RECIPIENT_EMAIL]

                logger.info("Sending the daily word email...")
                send_query_email(subject, message, recipient_list)
                logger.info("Daily word email sent successfully.")
            else:
                logger.warning("No word received from the prompt service.")

        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
