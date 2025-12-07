from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from db_helper import get_books, get_articles, get_inproceedings

class BibtexFile:
    def __init__(self):
        self.data = BibDatabase()
        self.data.entries = []


    def add_book(self, id, book):
        self.data.entries.append({
            'ID': id,
            'ENTRYTYPE': 'book',
            'title': book[1],
            'writer': book[2],
            'year': book[3],
            'isbn': book[4],
            'publisher': book[5]
        })

    def add_article(self, id, article):
        self.data.entries.append({
            'ID': id,
            'ENTRYTYPE': 'article',
            'title': article[1],
            'writer': article[2],
            'year': article[3],
            'DOI': article[4],
            'journal': article[5],
            'volume': article[6],
            'pages': article[7]
        })


    def add_inproceeding(self, id, inpro):
        self.data.entries.append({
            'ID': id,
            'ENTRYTYPE': 'inproceedings',
            'title': inpro[1],
            'writer': inpro[2],
            'year': inpro[3],
            'booktitle': inpro[4]
        })

    def get_file_content(self):
        writer = BibTexWriter()
        writer.indent = '    '
        writer.comma_first = False

        with open('library.bib', 'w', encoding='utf-8') as bibfile:
            bibfile.write(writer.write(self.data))
        with open('library.bib', 'r', encoding='utf-8') as bibfile:
            bibtex_content = bibfile.read()
        return bibtex_content
