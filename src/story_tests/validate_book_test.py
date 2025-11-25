import unittest
from util import validate_book, UserInputError

class TestTodoValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_too_short_title_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("", "author", 2020, "1234567890", "publisher")

    def test_too_long_title_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("A" * 21, "author", 2020, "1234567890", "publisher")

    def test_negative_year_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("Valid Title", "author", -1990, "1234567890", "publisher")