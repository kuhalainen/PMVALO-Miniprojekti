import os
from sqlalchemy import text
from config import db, app


# Utility functions for database management
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

def setup_db():
    """
      Creating the database
      If database tables already exist, those are dropped before the creation
    """
    tables_in_db = tables()
    if len(tables_in_db) > 0:
        print(f"Tables exist, dropping: {', '.join(tables_in_db)}")
        for table in tables_in_db:
            sql = text(f"DROP TABLE {table}")
            db.session.execute(sql)
        db.session.commit()

    print("Creating database")

    # Read schema from schema.sql file
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read().strip()

    sql = text(schema_sql)
    db.session.execute(sql)
    db.session.commit()

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

def get_book(book_id):
    sql = text("SELECT books.id, books.title, books.writer, books.year, " \
    "books.isbn, books.publisher FROM books WHERE books.id = :id ")
    return db.session.execute(sql, {"id": book_id}).fetchone()

def get_article(article_id):

    sql = text("SELECT articles.id, articles.title, articles.writer, articles.year," \
    " articles.doi, articles.journal FROM articles WHERE articles.id = :id ")

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
        all_items.sort(key=lambda x: x[2])  # Sort by writer (index 2)
    elif sort == 'year':
        all_items.sort(key=lambda x: x[3], reverse=True)  # Sort by year (index 3) descending
    #elif sort ==


    return all_items
    #if sort == 'author':
        #sql = text(
            #"SELECT * FROM books " \
            #"UNION ALL SELECT * FROM articles " \
            #"UNION ALL SELECT * FROM inproceedings " \
            #"ORDER BY writer ASC"
       # )
    #elif sort == 'year':
        #sql = text(
            #"SELECT * FROM books" \
            #" UNION ALL SELECT * FROM articles" \
            #" UNION ALL SELECT * FROM inproceedings " \
            #"ORDER BY year ASC"
       # )
    #else:
        #sql = text(
            #3#"SELECT * FROM books " \
            #"UNION ALL SELECT * FROM articles " \
            #"UNION ALL SELECT * FROM inproceedings ")
    
    #sql = text(
        #"SELECT books.id AS id, " \
        #"books.title AS title, " \
        #"books.writer AS writer, " \
        #"books.year AS year, "
        #"'book' AS type FROM books "
        #"UNION "
        #"SELECT articles.id AS id, " \
        #"articles.title AS title, " \
        #"articles.writer AS writer, " \
        #"articles.year AS year, "
        #"'article' AS type FROM articles "
        #"UNION "
        #"SELECT inproceedings.id AS id, " \
        #"inproceedings.title AS title, " \
        #"inproceedings.writer AS writer, " \
        #"inproceedings.year AS year, "
        #"'inproceeding' AS type FROM inproceedings "
        #"ORDER BY title ASC"
    #)
    #return db.session.execute(sql).fetchall()

def delete_book(book_id):
    sql = text("DELETE FROM books WHERE id = :id")
    db.session.execute(sql, {'id': book_id})
    db.session.commit()

def delete_article(article_id):
    sql = text("DELETE FROM articles WHERE id = :id")
    db.session.execute(sql, {'id': article_id})
    db.session.commit()

def delete_inproceeding(inproceeding_id):
    sql = text("DELETE FROM inproceedings WHERE id = :id")
    db.session.execute(sql, {'id': inproceeding_id})
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        setup_db()
