import unittest
from bibtex_gen import BibtexFile

class TestBibtex(unittest.TestCase):
    
    def setUp(self):
        self.book = [1, 'Testikirja', 'Kirjoittaja', '2005', '9780128043388', 'Testipublisher']
        self.article = [1, 'Testiartikkeli', 'Kirjoittaja', '2005', '10.1145/3366423', 'Testijournal', '5', '1-5']
        self.inproceeding = [1, 'Testiinproceeding', 'Kirjoittaja', '2005', 'Otsikko']
    
    def test_correct_books(self):
        file = BibtexFile()
        file.add_book('151', self.book)
        content = file.get_file_content()
        self.assertEqual(content, """@book{151,
    isbn = {9780128043388},
    publisher = {Testipublisher},
    title = {Testikirja},
    writer = {Kirjoittaja},
    year = {2005}
}
""")
        
    def test_correct_articles(self):
        file = BibtexFile()
        file.add_article('151', self.article)
        content = file.get_file_content()
        self.assertEqual(content, """@article{151,
    DOI = {10.1145/3366423},
    journal = {Testijournal},
    pages = {1-5},
    title = {Testiartikkeli},
    volume = {5},
    writer = {Kirjoittaja},
    year = {2005}
}
""")
    def test_correct_inproceedings(self):
        file = BibtexFile()
        file.add_inproceeding('151', self.inproceeding)
        content = file.get_file_content()
        self.assertEqual(content, """@inproceedings{151,
    booktitle = {Otsikko},
    title = {Testiinproceeding},
    writer = {Kirjoittaja},
    year = {2005}
}
""")