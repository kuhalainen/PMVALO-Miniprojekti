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

def get_books():
    sql = text("SELECT * FROM books ORDER BY title ASC")
    return db.session.execute(sql).fetchall()

def get_articles():
    sql = text("SELECT * FROM articles ORDER BY title ASC")
    return db.session.execute(sql).fetchall()

def get_book(book_id):
    sql = text("SELECT books.id, books.title, books.writer, books.year, " \
    "books.isbn, books.publisher FROM books WHERE books.id = :id ")
    return db.session.execute(sql, {"id": book_id}).fetchone()

def get_article(article_id):

    sql = text("SELECT articles.id, articles.title, articles.writer, articles.year," \
    " articles.doi, articles.journal FROM articles WHERE articles.id = :id ")

    return db.session.execute(sql, {"id": article_id}).fetchone()

if __name__ == "__main__":
    with app.app_context():
        setup_db()
