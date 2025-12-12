import unittest
from util import validate_book, validate_article, validate_inproceedings, UserInputError

class TestValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_too_short_title_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("", "author", 2020, "1234567890", "publisher")

    def test_too_long_title_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("A" * 101, "author", 2020, "1234567890", "publisher")

    def test_negative_year_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("Valid Title", "author", -1990, "1234567890", "publisher")

    def test_non_four_digit_year_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("Valid Title", "author", 99, "1234567890", "publisher")

    def test_year_cant_be_set_to_future(self):
        with self.assertRaises(UserInputError):
            validate_book("Valid Title", "author", 3000, "1234567890", "publisher")

    def test_invalid_isbn_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("Valid Title", "author", 2020, "invalid_isbn", "publisher")
    
    def test_isbn_wrong_length_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_book("Valid Title", "author", 2020, "123456789", "publisher")
        with self.assertRaises(UserInputError):
            validate_book("Valid Title", "author", 2020, "123456789012", "publisher")

    def test_valid_input_does_not_raise_error(self):
        try:
            validate_book("Valid Title", "author", 2020, "1234567890", "publisher")
        except UserInputError:
            self.fail("validate_book() raised UserInputError unexpectedly!")


    def test_empty_article_author_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_article("Valid Title", "", 2020)

    def test_article_title_too_short_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_article("Shrt", "author", 2020)

    def test_article_title_too_long_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_article("A" * 101, "author", 2020)     

    def test_article_negative_year_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_article("Valid Title", "author", -2020)

    def test_article_non_four_digit_year_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_article("Valid Title", "author", 99)

    def test_article_year_cant_be_set_to_future(self):
        with self.assertRaises(UserInputError):
            validate_article("Valid Title", "author", 3000)
    

    def test_empty_inproceedings_fields_raise_error(self):
        with self.assertRaises(UserInputError):
            validate_inproceedings("", "author", "booktitle", 2020)
        with self.assertRaises(UserInputError):
            validate_inproceedings("Valid Title", "", "booktitle", 2020)
        with self.assertRaises(UserInputError):
            validate_inproceedings("Valid Title", "author", "", 2020)
        with self.assertRaises(UserInputError):
            validate_inproceedings("Valid Title", "author", "booktitle", "")

    def test_inproceedings_year_negative_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_inproceedings("Valid Title", "author", "booktitle", -2020)

    def test_inproceedings_non_four_digit_year_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_inproceedings("Valid Title", "author", "booktitle", 99)

    def test_inproceedings_year_cant_be_set_to_future(self):
        with self.assertRaises(UserInputError):
            validate_inproceedings("Valid Title", "author", "booktitle", 3000)  