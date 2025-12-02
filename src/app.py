
from flask import Flask, redirect, render_template, request, jsonify, flash, send_file
import io
from config import db
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from config import app, test_env
from util import UserInputError, validate_book
import os
from dotenv import load_dotenv
from flask import redirect, render_template, request, jsonify, flash
from config import text, db, app, test_env
import db_helper
from bibtex_gen import gen_bibtex


load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    print("WARNING: Secret key not found. Check your .env file.")

@app.route("/")
def index():
    selected = request.args.get('category', 'all')
    sort = request.args.get('sort', 'default')

    if selected == 'books':
        items = db_helper.get_books(sort)
        countitems = len(items)
    elif selected == 'articles':
        items = db_helper.get_articles(sort)
        countitems = len(items)
    elif selected == 'inproceedings':
        items = db_helper.get_inproceedings(sort)
        countitems = len(items)
    else:
        items = db_helper.get_all_references(sort)
        countitems = len(items)
    return render_template("index.html", items = items, countitems = countitems, selected=selected, sort=sort)

@app.route('/books/new')
def new_book():
    return render_template('book_form.html')

@app.route('/articles/new')
def new_article():
    return render_template('article_form.html')

@app.route('/inproceedings/new')
def new_inproceeding():
    return render_template('inproceeding_form.html')

@app.route('/books/create', methods=['POST'])
def create_book():
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')
    isbn = request.form.get('isbn')
    publisher = request.form.get('publisher')

    # Minimal validation: title and author required
    try:
        validate_book(title, author, year, isbn, publisher)
    except UserInputError as e:
        flash(str(e), 'error')
        return redirect('/books/new')
    except ValueError as e:
        flash(str(e), 'error')
        return redirect('/books/new')

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

@app.route('/inproceedings/create', methods=['POST'])
def create_inproceeding():
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')
    booktitle = request.form.get('booktitle')

    # Minimal validation: title and author required
    if not title or not author:
        flash('Title and author are required.', 'error')
        return redirect('/inproceedings/new')

    sql = text("INSERT INTO inproceedings (title, writer, year, booktitle)" \
    "VALUES (:title, :writer, :year, :booktitle)")
    db.session.execute(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'booktitle': booktitle,
    })
    db.session.commit()

    flash('Konferenssijulkaisun Artikkeli lisätty onnistuneesti', 'success')
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

@app.route('/remove_book/<int:book_id>', methods=['GET', 'POST'])
def remove_book(book_id):
    book = db_helper.get_book(book_id)

    if request.method == 'GET':
        return render_template('remove_book.html', book=book)
    if request.method == 'POST':
        if "remove" in request.form:
            db_helper.delete_book(book_id)
            flash('Kirja poistettu onnistuneesti', 'success')
            return redirect('/')
        return redirect('/book/' + str(book_id))

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


@app.route('/remove_article/<int:article_id>', methods=['GET', 'POST'])
def remove_article(article_id):
    article = db_helper.get_article(article_id)

    if request.method == 'GET':
        return render_template('remove_article.html', article=article)
    if request.method == 'POST':
        if "remove" in request.form:
            db_helper.delete_article(article_id)
            flash('Artikkeli poistettu onnistuneesti', 'success')
            return redirect('/')
        return redirect('/article/' + str(article_id))

@app.route('/inproceeding/<int:inproceeding_id>')
def inproceeding(inproceeding_id):
    current_inproceeding = db_helper.get_inproceeding(inproceeding_id)

    return render_template("/inproceeding.html", inproceeding=current_inproceeding)

@app.route('/edit_inproceeding/<int:inproceeding_id>')
def edit_inproceeding(inproceeding_id):
    current_inproceeding = db_helper.get_inproceeding(inproceeding_id)

    return render_template('edit_inproceeding.html', inproceeding=current_inproceeding)

@app.route('/inproceedings/edit/<int:inproceeding_id>', methods=['POST'])
def edit_inproceeding_post(inproceeding_id):
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')
    booktitle = request.form.get('booktitle')

    # Minimal validation: title and author required
    if not title or not author:
        flash('Title and author are required.', 'error')
        return redirect(f'/edit_inproceeding/{inproceeding_id}')

    sql = text("UPDATE inproceedings SET title = :title, writer = :writer," \
    " year = :year, booktitle = :booktitle WHERE id = :id")
    db.session.execute(sql, {
       'title': title,
       'writer': author,
       'year': year,
       'booktitle': booktitle,
       'id': inproceeding_id
    })
    db.session.commit()

    flash('Konferenssijulkaisun artikkelin tiedot päivitetty onnistuneesti', 'success')
    return redirect('/')

@app.route('/remove_inproceeding/<int:inproceeding_id>', methods=['GET', 'POST'])
def remove_inproceeding(inproceeding_id):
    inproceeding = db_helper.get_inproceeding(inproceeding_id)

    if request.method == 'GET':
        return render_template('remove_inproceeding.html', inproceeding=inproceeding)
    if request.method == 'POST':
        if "remove" in request.form:
            db_helper.delete_inproceeding(inproceeding_id)
            flash('Konferenssijulkaisun artikkeli poistettu onnistuneesti', 'success')
            return redirect('/')
        return redirect('/inproceeding/' + str(inproceeding_id))
    
@app.route('/inspect_bibtex')
def inspect_bibtex():
    content = gen_bibtex()

    proxy_file = io.BytesIO(content.encode('utf-8'))
    
    return send_file(
        proxy_file,
        mimetype='text/x-bibtex',
        as_attachment=False,
        download_name='references.bib'
    )

@app.route('/download_bibtex')
def download_bibtex():
    content = gen_bibtex()

    proxy_file = io.BytesIO(content.encode('utf-8'))
    
    return send_file(
        proxy_file,
        mimetype='text/x-bibtex',
        as_attachment=True,
        download_name='references.bib'
    )

if test_env:
    @app.route("/reset_db")
    def reset_database():
        db_helper.reset_db()
        return jsonify({ 'message': "db reset" })
