from ..models import Word
import logging
import re

logger = logging.getLogger(__name__)


def extract_word(response_text):
    try:
        match = re.search(r'Word:\s*([^\s\(]+)', response_text)
        if match:
            return match.group(1).strip()
        else:
            logger.warning("Word not found in the response.")
            return None
    except Exception as e:
        logger.exception("An error occurred in extract_word")
        return None


def store_word(response_text, language="Japanese"):
    try:
        word = extract_word(response_text)
        if word:
            new_word = Word(word=word, language=language)
            new_word.save()
            logger.info(f"The word '{word}' has been successfully stored.")
        else:
            logger.warning("No word extracted to store.")
    except Exception as e:
        logger.exception("An error occurred while storing the word")
