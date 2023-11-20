from django.test import TestCase
from django.conf import settings
from ..services.word_service import extract_word, store_word
from ..models import Word
import os


class ExtractWordTests(TestCase):

    # word is parsed with parentheses
    def test_extract_word_with_parentheses(self):
        response = "Word: Cat (Ka-tuh)"
        extracted_word = extract_word(response)
        self.assertEqual(extracted_word, "Cat")

    # word is parsed without parentheses
    def test_extract_word_without_parentheses(self):
        response = "Word: Cat"
        extracted_word = extract_word(response)
        self.assertEqual(extracted_word, "Cat")

    # word is not found
    def test_extract_word_not_found(self):
        response = "No word here"
        extracted_word = extract_word(response)
        self.assertIsNone(extracted_word)


class StoreWordTests(TestCase):

    def setUp(self):
        settings.TARGET_LANGUAGE = "Spanish"

    def tearDown(self):
        del settings.TARGET_LANGUAGE

    # word is stored successfully
    def test_store_word_success(self):
        response_text = "Word: Cat (Ka-tuh)"
        store_word(response_text)
        saved_word = Word.objects.last()
        self.assertIsNotNone(saved_word)
        self.assertEqual(saved_word.word, "Cat")
        self.assertEqual(saved_word.language, "Spanish")

    # no word exists
    def test_store_word_no_word(self):
        response_text = "No word here"
        store_word(response_text)
        saved_word = Word.objects.last()
        self.assertIsNone(saved_word)
