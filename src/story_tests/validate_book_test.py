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

    def test_non_four_digit_year_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("Valid Title", "author", 99, "1234567890", "publisher")

    def test_invalid_isbn_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("Valid Title", "author", 2020, "invalid_isbn", "publisher")
    
    def test_isbn_wrong_length_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("Valid Title", "author", 2020, "123456789", "publisher")  # 9 digits
        with self.assertRaises(UserInputError):
            validate_book("Valid Title", "author", 2020, "123456789012", "publisher")  # 12 digits

    def test_valid_input_does_not_raise_error(self):
        try:
            validate_book("Valid Title", "author", 2020, "1234567890", "publisher")
        except UserInputError:
            self.fail("validate_book() raised UserInputError unexpectedly!")