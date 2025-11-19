from flask import Flask, redirect, render_template, request, jsonify, flash
from config import db
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from config import app, test_env
from util import validate_todo
import os
from dotenv import load_dotenv

app = Flask(__name__)
from config import text



from config import text


load_dotenv()

app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    print("WARNING: Secret key not found. Check your .env file.")

@app.route("/")

def index():
    sql = text("SELECT * FROM items")
    query = db.session.execute(sql)
    items = query.fetchall()
    books = []
    for item in items:
        book = f'{item[1]}, Author: {item[2]}, year: {item[3]}, ISBN: {item[4]}, Publisher: {item[5]}'
        books.append(book)
    return render_template("index.html", items=books)



@app.route('/books/new')
def new_book():
    return render_template('book_form.html')


@app.route('/books/create', methods=['POST'])
def create_book():
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')
    isbn = request.form.get('isbn')
    publisher = request.form.get('publisher')

    # Minimal validation: title and author required
    if not title or not author:
        flash('Title and author are required.', 'error')
        return redirect('/books/new')

    sql = text("INSERT INTO items (title, writer, year, isbn, publisher) VALUES (:title, :writer, :year, :isbn, :publisher)")
    db.session.execute(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'isbn': isbn,
       'publisher': publisher
    })
    db.session.commit()

    return redirect('/')
