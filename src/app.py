from flask import Flask, redirect, render_template, request, jsonify, flash
from config import db
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from config import app, test_env
from util import validate_todo
import os
from dotenv import load_dotenv
from config import text
import db_helper


load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    print("WARNING: Secret key not found. Check your .env file.")

@app.route("/")

def index():
    books = db_helper.get_books()
    articles = db_helper.get_articles()

    return render_template("index.html", books=books, articles = articles)


@app.route('/books/new')
def new_book():
    return render_template('book_form.html')


@app.route('/articles/new')
def new_article():
    return render_template('article_form.html')


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

    sql = text("INSERT INTO books (title, writer, year, isbn, publisher) VALUES (:title, :writer, :year, :isbn, :publisher)")
    db.session.execute(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'isbn': isbn,
       'publisher': publisher
    })
    db.session.commit()

    flash('Kirja lisätty onnistuneesti', 'success')
    return redirect('/')

@app.route('/articles/create', methods=['POST'])
def create_article():
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')
    doi = request.form.get('DOI')
    journal = request.form.get('journal')
    volume = request.form.get('volume')
    pages = request.form.get('pages')

    # Minimal validation: title and author required
    if not title or not author:
        flash('Title and author are required.', 'error')
        return redirect('/books/new')
    
    sql = text("INSERT INTO articles (title, writer, year, DOI, journal, volume, pages) VALUES (:title, :writer, :year, :DOI, :journal, :volume, :pages)")
    db.session.execute(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'DOI': doi,
       'journal': journal,
       'volume': volume,
       'pages': pages
    })
    db.session.commit()

    flash('Artikkeli lisätty onnistuneesti', 'success')
    return redirect('/')

@app.route('/book/<int:book_id>')
def book(book_id):

    book = db_helper.get_book(book_id)

    return render_template("/book.html", book = book)

if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
