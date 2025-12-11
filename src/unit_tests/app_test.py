import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()

    def test_new_book_returns_200(self):
        response = self.client.get('/books/new')
        self.assertEqual(response.status_code, 200)

    def test_new_book_contains_form(self):
        response = self.client.get('/books/new')
        self.assertIn(b'<form', response.data)
        self.assertIn(b'name="title"', response.data)
        self.assertIn(b'name="author"', response.data)
        self.assertIn(b'name="year"', response.data)
        self.assertIn(b'name="isbn"', response.data)
        self.assertIn(b'name="publisher"', response.data)

    def test_new_article_returns_200(self):
        response = self.client.get('/articles/new')
        self.assertEqual(response.status_code, 200)

    def test_new_inproceeding_returns_200(self):
        response = self.client.get('/inproceedings/new')
        self.assertEqual(response.status_code, 200)

    def test_inspect_bibtex_returns_200(self):
        response = self.client.get('/inspect_bibtex')
        self.assertEqual(response.status_code, 200)

    def test_index_sort_query_returns_200(self):
        resp = self.client.get('/?sort=author')
        self.assertEqual(resp.status_code, 200)

    def test_download_bibtex_returns_200(self):
        response = self.client.get('/download_bibtex')
        self.assertEqual(response.status_code, 200)
