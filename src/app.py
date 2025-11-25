<<<<<<< HEAD
=======
from flask import Flask, redirect, render_template, request, jsonify, flash
from config import db
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from config import app, test_env
from util import validate_book
>>>>>>> f54591d (unittests to validate book title and year)
import os
from dotenv import load_dotenv
from flask import redirect, render_template, request, jsonify, flash
from config import text, db, app, test_env
import db_helper


load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    print("WARNING: Secret key not found. Check your .env file.")

@app.route("/")
def index():
    books = db_helper.get_books()
    countbooks = len(books)
    articles = db_helper.get_articles()
    countarticles = len(articles)

    return render_template("index.html", books=books, articles = articles,
                            countbooks = countbooks, countarticles = countarticles)


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
    validate_book(title, author, year, isbn, publisher)

    if not title or not author:
        flash('Title and author are required.', 'error')
        return redirect('/books/new')

    sql = text("INSERT INTO books (title, writer, year, isbn," \
    " publisher) VALUES (:title, :writer, :year, :isbn, :publisher)")
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

    sql = text("INSERT INTO articles (title, writer, year, DOI," \
    " journal, volume, pages) VALUES (:title, :writer, :year, :DOI, :journal, :volume, :pages)")
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
    current_book = db_helper.get_book(book_id)

    return render_template("/book.html", book=current_book)

@app.route('/edit_book/<int:book_id>')
def edit_book(book_id):
    current_book = db_helper.get_book(book_id)

    return render_template('edit_book.html', book=current_book)

@app.route('/books/edit/<int:book_id>', methods=['POST'])
def edit_book_post(book_id):
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')
    isbn = request.form.get('isbn')
    publisher = request.form.get('publisher')

    # Minimal validation: title and author required
    if not title or not author:
        flash('Title and author are required.', 'error')
        return redirect(f'/edit_book/{book_id}')

    sql = text("UPDATE books SET title = :title, writer = :writer," \
    " year = :year, isbn = :isbn, publisher = :publisher WHERE id = :id")
    db.session.execute(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'isbn': isbn,
       'publisher': publisher,
       'id': book_id
    })
    db.session.commit()

    flash('Kirjan tiedot päivitetty onnistuneesti', 'success')
    return redirect('/')

@app.route('/article/<int:article_id>')
def article(article_id):
    current_article = db_helper.get_article(article_id)

    return render_template("/article.html", article=current_article)

@app.route('/edit_article/<int:article_id>')
def edit_article(article_id):
    current_article = db_helper.get_article(article_id)

    return render_template('edit_article.html', article=current_article)

@app.route('/articles/edit/<int:article_id>', methods=['POST'])
def edit_article_post(article_id):
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
        return redirect(f'/edit_article/{article_id}')

    sql = text("UPDATE articles SET title = :title, writer = :writer," \
    " year = :year, DOI = :doi, journal = :journal, volume = :volume," \
    " pages = :pages WHERE id = :id")
    db.session.execute(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'doi': doi,
       'journal': journal,
       'volume' : volume,
       'pages' : pages,
       'id': article_id
    })
    db.session.commit()

    flash('Artikkelin tiedot päivitetty onnistuneesti', 'success')
    return redirect('/')

if test_env:
    @app.route("/reset_db")
    def reset_database():
        db_helper.reset_db()
        return jsonify({ 'message': "db reset" })
