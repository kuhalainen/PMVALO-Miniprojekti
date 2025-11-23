from config import db, app
from sqlalchemy import text
from db import query
import os

def reset_db():
  print(f"Clearing contents from table todos")
  sql = text(f"DELETE FROM todos")
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

def get_items():
    sql = text("SELECT * FROM items ORDER BY title ASC")
    return db.session.execute(sql).fetchall()

def get_articles():
    sql = text("SELECT * FROM articles ORDER BY title ASC")
    return db.session.execute(sql).fetchall()

def get_item(item_id):
    sql = text("SELECT items.id, items.title, items.writer, items.year, items.isbn, items.publisher FROM items WHERE items.id = :id ")
    return db.session.execute(sql, {"id": item_id}).fetchone()

if __name__ == "__main__":
    with app.app_context():
      setup_db()

