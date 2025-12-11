import os
from sqlalchemy import text
from config import db, app


def reset_db():
    print("Clearing contents from tables books and articles")
    for t in tables():
        sql = text(f"DELETE FROM {t}")
        db.session.execute(sql)
        db.session.commit()

def tables():
    """Returns all table names from the database except those ending with _id_seq"""
    sql = text(
      "SELECT table_name "
      "FROM information_schema.tables "
      "WHERE table_schema = 'public' "
      "AND table_name NOT LIKE '%_id_seq'"
    )

    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]

def db_execute_insert(sql, dictionary):
    db.session.execute(sql, dictionary)
    db.session.commit()

def setup_db():

    tables_in_db = tables()
    if len(tables_in_db) > 0:
        print(f"Tables exist, dropping: {', '.join(tables_in_db)}")
        for table in tables_in_db:
            sql = text(f"DROP TABLE {table}")
            db.session.execute(sql)
        db.session.commit()

    print("Creating database")

    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read().strip()

    db.session.execute(text(schema_sql))
    db.session.commit()

def insert_book(title, author, year, isbn, publisher):
    sql = text("INSERT INTO books (title, writer, year, isbn," \
    " publisher) VALUES (:title, :writer, :year, :isbn, :publisher)")
    db_execute_insert(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'isbn': isbn,
       'publisher': publisher
    })

def insert_article(title, author, year, doi, journal, volume, pages):
    sql = text("INSERT INTO articles (title, writer, year, DOI," \
    " journal, volume, pages) VALUES (:title, :writer, :year, :DOI, :journal, :volume, :pages)")
    db_execute_insert(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'DOI': doi,
       'journal': journal,
       'volume': volume,
       'pages': pages
    })

def insert_inrproceedings(title, author, year, booktitle):
    sql = text("INSERT INTO inproceedings (title, writer, year, booktitle)" \
    "VALUES (:title, :writer, :year, :booktitle)")
    db_execute_insert(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'booktitle': booktitle,
    })

def get_books(sort='default'):
    sql = text("SELECT books.id AS id, " \
        "books.title AS title, " \
        "books.writer AS writer, " \
        "books.year AS year, " \
        "books.isbn AS isbn, " \
        "books.publisher AS publisher, " \
        "'book' AS type FROM books ")
    books = db.session.execute(sql).fetchall()
    if sort == 'author':
        books.sort(key=lambda x: x[2])
    elif sort == 'year':
        books.sort(key=lambda x: x[3], reverse=True)

    return books

def get_articles(sort='default'):
    sql = text("SELECT articles.id AS id, " \
        "articles.title AS title, " \
        "articles.writer AS writer, " \
        "articles.year AS year, " \
        "articles.doi AS doi, " \
        "articles.journal AS journal, " \
        "articles.volume AS volume, " \
        "articles.pages AS pages, " \
        "'article' AS type FROM articles ORDER BY title ASC")
    articles = db.session.execute(sql).fetchall()
    if sort == 'author':
        articles.sort(key=lambda x: x[2])
    elif sort == 'year':
        articles.sort(key=lambda x: x[3], reverse=True)

    return articles

def get_inproceedings(sort='default'):
    sql = text("SELECT inproceedings.id AS id, " \
        "inproceedings.title AS title, " \
        "inproceedings.writer AS writer, " \
        "inproceedings.year AS year, " \
        "inproceedings.booktitle AS booktitle, " \
        "'inproceeding' AS type FROM inproceedings ORDER BY title ASC")
    inproceedings = db.session.execute(sql).fetchall()
    if sort == 'author':
        inproceedings.sort(key=lambda x: x[2])
    elif sort == 'year':
        inproceedings.sort(key=lambda x: x[3], reverse=True)

    return inproceedings

def update_book(title, author, year, isbn, publisher, book_id):
    sql = text("UPDATE books SET title = :title, writer = :writer," \
    " year = :year, isbn = :isbn, publisher = :publisher WHERE id = :id")
    db_execute_insert(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'isbn': isbn,
       'publisher': publisher,
       'id': book_id
    })

def update_article(title, author, year, doi, journal, volume, pages, article_id):
    sql = text("UPDATE articles SET title = :title, writer = :writer," \
    " year = :year, DOI = :doi, journal = :journal, volume = :volume," \
    " pages = :pages WHERE id = :id")
    db_execute_insert(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'doi': doi,
       'journal': journal,
       'volume' : volume,
       'pages' : pages,
       'id': article_id
    })

def update_inproceedings(title, author, year, booktitle, inproceeding_id):
    sql = text("UPDATE inproceedings SET title = :title, writer = :writer," \
    " year = :year, booktitle = :booktitle WHERE id = :id")
    db_execute_insert(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'booktitle': booktitle,
       'id': inproceeding_id
    })

def get_book(book_id):
    sql = text("SELECT books.id, books.title, books.writer, books.year, " \
    "books.isbn, books.publisher FROM books WHERE books.id = :id ")
    return db.session.execute(sql, {"id": book_id}).fetchone()

def get_article(article_id):

    sql = text("SELECT articles.id, articles.title, articles.writer, articles.year," \
    " articles.doi, articles.journal, articles.volume, articles.pages FROM articles WHERE articles.id = :id ")

    return db.session.execute(sql, {"id": article_id}).fetchone()

def get_inproceeding(inproceedings_id):

    sql = text("SELECT inproceedings.id, inproceedings.title, inproceedings.writer, inproceedings.year," \
    " inproceedings.booktitle FROM inproceedings WHERE inproceedings.id = :id ")

    return db.session.execute(sql, {"id": inproceedings_id}).fetchone()

def get_all_references(sort='default'):
    books_sql = text("SELECT id, title, writer, year, 'book' as type FROM books")
    articles_sql = text("SELECT id, title, writer, year, 'article' as type FROM articles")
    inproceedings_sql = text("SELECT id, title, writer, year, 'inproceeding' as type FROM inproceedings")

    books = db.session.execute(books_sql).fetchall()
    articles = db.session.execute(articles_sql).fetchall()
    inproceedings = db.session.execute(inproceedings_sql).fetchall()

    all_items = list(books) + list(articles) + list(inproceedings)

    if sort == 'author':
        all_items.sort(key=lambda x: x[2])
    elif sort == 'year':
        all_items.sort(key=lambda x: x[3], reverse=True)

    return all_items

def delete_book(book_id):
    db_execute_insert(text("DELETE FROM books WHERE id = :id"), {'id': book_id})

def delete_article(article_id):
    db_execute_insert(text("DELETE FROM articles WHERE id = :id"), {'id': article_id})

def delete_inproceeding(inproceeding_id):
    db_execute_insert(text("DELETE FROM inproceedings WHERE id = :id"), {'id': inproceeding_id})


if __name__ == "__main__":
    with app.app_context():
        setup_db()
