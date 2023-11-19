from django.utils import timezone
from django.test import TestCase
from ..models import Word


class WordModelTests(TestCase):

    # set up data for the TestCase
    def setUp(self):
        self.word = Word.objects.create(word="Test", language="English")

    # test the word field
    def test_word_field(self):
        self.assertEqual(self.word.word, "Test")

    # test the language field
    def test_language_field(self):
        self.assertEqual(self.word.language, "English")

    # test the created_on field
    def test_created_on_field(self):
        self.assertTrue(isinstance(self.word.created_on, timezone.datetime))
        self.assertTrue(self.word.created_on <= timezone.now())
