from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from config import db
from db_helper import get_books, get_articles, get_inproceedings
from secrets import token_hex
def gen_bibtex():
    data = BibDatabase()

    data.entries = []

    books = get_books()
    for book in books:
        data.entries.append({
            'ID': token_hex(5),
            'ENTRYTYPE': 'book',
            'title': book[1],
            'writer': book[2],
            'year': book[3],
            'isbn': book[4],
            'publisher': book[5]
        })
    articles = get_articles()
    for article in articles:
        data.entries.append({
            'ID': token_hex(5),
            'ENTRYTYPE': 'article',
            'title': article[1],
            'writer': article[2],
            'year': article[3],
            'DOI': article[4],
            'journal': article[5],
            'volume': article[6],
            'pages': article[7]
        })
    inproceedings = get_inproceedings()
    for inpro in inproceedings:
        data.entries.append({
            'ID': token_hex(5),
            'ENTRYTYPE': 'inproceedings',
            'title': inpro[1],
            'writer': inpro[2],
            'year': inpro[3],
            'booktitle': inpro[4]
        })
    writer = BibTexWriter()
    writer.indent = '    '     
    writer.comma_first = False 

    with open('library.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(data))
    with open('library.bib', 'r', encoding='utf-8') as bibfile:
        bibtex_content = bibfile.read()
    return bibtex_content