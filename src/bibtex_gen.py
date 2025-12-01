import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from config import db
from db_helper import get_books, get_articles, get_inproceedings
def gen_bibtex():
    data = BibDatabase()

    data.entries = []

    books = get_books()
    for book in books:
        data.entries.append({
            'title': book[1],
            'writer': book[2],
            'year': book[3],
            'isbn': book[4],
            'publisher': book[5]
        })

    writer = BibTexWriter()
    writer.indent = '    '     
    writer.comma_first = False 

    with open('library.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(data))