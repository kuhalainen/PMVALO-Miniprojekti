
from flask import Flask, redirect, render_template, request, jsonify, flash, send_file
import io
from db_helper import reset_db, get_books, get_articles, get_inproceedings
from repositories.todo_repository import get_todos, create_todo, set_done
from config import text, db, app, test_env
from util import UserInputError, validate_book, validate_article, validate_inproceedings
import os
from dotenv import load_dotenv
import db_helper
from bibtex_gen import BibtexFile
from secrets import token_hex

BOOK_FIELDS = [
    {"name": "title", "label": "Title", "type": "text", "required": True},
    {"name": "author", "label": "Author", "type": "text", "required": True},
    {"name": "year", "label": "Year", "type": "number"},
    {"name": "isbn", "label": "ISBN", "type": "text"},
    {"name": "publisher", "label": "Publisher", "type": "text"},
]

ARTICLE_FIELDS = [
    {"name": "title", "label": "Title", "type": "text", "required": True},
    {"name": "author", "label": "Author", "type": "text", "required": True},
    {"name": "year", "label": "Year", "type": "number", "inputmode": "numeric", "pattern": "[0-9]{4}"},
    {"name": "DOI", "label": "DOI", "type": "text"},
    {"name": "journal", "label": "Journal", "type": "text"},
    {"name": "volume", "label": "Volume", "type": "text"},
    {"name": "pages", "label": "Pages", "type": "text"},
]

INPROCEEDING_FIELDS = [
    {"name": "title", "label": "Title", "type": "text", "required": True},
    {"name": "booktitle", "label": "Booktitle", "type": "text"},
    {"name": "author", "label": "Author", "type": "text", "required": True},
    {"name": "year", "label": "Year", "type": "number", "inputmode": "numeric", "pattern": "[0-9]{4}"},
]

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    print("WARNING: Secret key not found. Check your .env file.")

@app.route("/")
def index():
    selected = request.args.get('category', 'all')
    sort = request.args.get('sort', 'default')
    search = request.args.get('search', None)

    if selected == 'books':
        items = db_helper.get_books(sort, search)
        countitems = len(items)
    elif selected == 'articles':
        items = db_helper.get_articles(sort, search)
        countitems = len(items)
    elif selected == 'inproceedings':
        items = db_helper.get_inproceedings(sort, search)
        countitems = len(items)
    else:
        items = db_helper.get_all_references(sort, search)
        countitems = len(items)
    return render_template("index.html", items = items,
                           countitems = countitems,
                           selected=selected,
                           sort=sort)

@app.route('/books/new')
def new_book():

    return render_template('reference_add.html',
                            title = "Lisää kirja",
                            fields=BOOK_FIELDS,
                            submit_button_text="Tallenna kirja",
                            submit_url="/books/create"
    )

@app.route('/articles/new')
def new_article():

    return render_template('reference_add.html',
                        title = "Lisää artikkeli",
                        fields=ARTICLE_FIELDS,
                        submit_button_text="Tallenna artikkeli",
                        submit_url="/articles/create"
    )

@app.route('/inproceedings/new')
def new_inproceeding():

    return render_template('reference_add.html',
                    title = "Lisää Konferenssijulkaisun artikkeli",
                    fields=INPROCEEDING_FIELDS,
                    submit_button_text="Tallenna Konferenssijulkaisun artikkeli",
                    submit_url="/inproceedings/create"
    )

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

    try:
        validate_article(title, author, year, doi, journal, volume, pages)
    except UserInputError as e:
        flash(str(e), 'error')
        return redirect('/articles/new')
    except ValueError as e:
        flash(str(e), 'error')
        return redirect('/articles/new')

    # Minimal validation: title and author required
    if not title or not author:
        flash('Title and author are required.', 'error')
        return redirect('/articles/new')

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

    try:
        validate_inproceedings(title, author, booktitle, year)
    except UserInputError as e:
        flash(str(e), 'error')
        return redirect('/inproceedings/new')
    except ValueError as e:
        flash(str(e), 'error')
        return redirect('/inproceedings/new')

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
    current_book_dict = dict(current_book._mapping)
    current_book_dict['author'] = current_book_dict.pop('writer')

    return render_template("/reference_show.html",
                            title = "Book",
                            reference=current_book_dict,
                            fields=BOOK_FIELDS,
                            edit_button_url=f"/edit_book/{book_id}",
                            remove_button_url=f"/remove_book/{book_id}")

@app.route('/edit_book/<int:book_id>')
def edit_book(book_id):
    current_book = db_helper.get_book(book_id)

    current_book_dict = dict(current_book._mapping)
    current_book_dict['author'] = current_book_dict.pop('writer')

    return render_template('reference_edit.html',
                            reference=current_book_dict,
                            title = "Muokkaa kirjaa",
                            fields=BOOK_FIELDS,
                            submit_button_text="Tallenna muutokset",
                            submit_button_url=f"/books/edit/{book_id}",
                            back_button_text="Takaisin kirjan sivulle",
                            back_button_url=f"/book/{book_id}"
    )

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
        prev = request.referrer
        return render_template('reference_remove.html',
                                reference=book,
                                title="Kirjan poisto",
                                conf_message="Haluatko varmasti poistaa tämän kirjan",
                                form_url=f"/remove_book/{book_id}",
                                remove_button_text="Poista kirja",
                                prev_url = prev
                                )

    if request.method == 'POST':
        prev_url = request.form.get('prev_url')
        if "remove" in request.form:
            db_helper.delete_book(book_id)
            flash('Kirja poistettu onnistuneesti', 'success')
            return redirect('/')
        return redirect(prev_url or '/')

@app.route('/article/<int:article_id>')
def article(article_id):
    current_article = db_helper.get_article(article_id)

    current_article_dict = dict(current_article._mapping)
    current_article_dict['author'] = current_article_dict.pop('writer')
    current_article_dict['DOI'] = current_article_dict.pop('doi')

    return render_template("/reference_show.html",
                            title = "Article",
                            reference=current_article_dict,
                            fields=ARTICLE_FIELDS,
                            edit_button_url=f"/edit_article/{article_id}",
                            remove_button_url=f"/remove_article/{article_id}")

@app.route('/edit_article/<int:article_id>')
def edit_article(article_id):
    current_article = db_helper.get_article(article_id)

    current_article_dict = dict(current_article._mapping)
    current_article_dict['author'] = current_article_dict.pop('writer')
    current_article_dict['DOI'] = current_article_dict.pop('doi')

    return render_template('reference_edit.html',
                            reference=current_article_dict,
                            title = "Muokkaa artikkelia",
                            fields=ARTICLE_FIELDS,
                            submit_button_text="Tallenna muutokset",
                            submit_button_url=f"/articles/edit/{article_id}",
                            back_button_text="Takaisin artikkelin sivulle",
                            back_button_url=f"/article/{article_id}"
    )

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
        prev = request.referrer
        return render_template('reference_remove.html',
                        reference=article,
                        title="Artikkelin poisto",
                        conf_message="Haluatko varmasti poistaa tämän artikkelin?",
                        form_url=f"/remove_article/{article_id}",
                        remove_button_text="Poista artikkeli",
                        prev_url = prev
                        )

    if request.method == 'POST':
        prev_url = request.form.get('prev_url')
        if "remove" in request.form:
            db_helper.delete_article(article_id)
            flash('Artikkeli poistettu onnistuneesti', 'success')
            return redirect('/')
        return redirect(prev_url or '/')

@app.route('/inproceeding/<int:inproceeding_id>')
def inproceeding(inproceeding_id):
    current_inproceeding = db_helper.get_inproceeding(inproceeding_id)

    current_inproceeding_dict = dict(current_inproceeding._mapping)
    current_inproceeding_dict['author'] = current_inproceeding_dict.pop('writer')
    #current_inproceeding_dict['DOI'] = current_inproceeding_dict.pop('doi')

    return render_template("/reference_show.html",
                            title = "Inproceeding",
                            reference=current_inproceeding_dict,
                            fields=INPROCEEDING_FIELDS,
                            edit_button_url=f"/edit_inproceeding/{inproceeding_id}",
                            remove_button_url=f"/remove_inproceeding/{inproceeding_id}")

@app.route('/edit_inproceeding/<int:inproceeding_id>')
def edit_inproceeding(inproceeding_id):
    current_inproceeding = db_helper.get_inproceeding(inproceeding_id)

    current_inproceeding_dict = dict(current_inproceeding._mapping)
    current_inproceeding_dict['author'] = current_inproceeding_dict.pop('writer')
    #current_inproceeding_dict['DOI'] = current_inproceeding_dict.pop('doi')

    return render_template('reference_edit.html',
                        reference=current_inproceeding_dict,
                        title = "Muokkaa konferenssinjulkaisun artikkelia",
                        fields=INPROCEEDING_FIELDS,
                        submit_button_text="Tallenna muutokset",
                        submit_button_url=f"/inproceedings/edit/{inproceeding_id}",
                        back_button_text="Takaisin konferenssinjulkaisun artikkelin sivulle",
                        back_button_url=f"/inproceeding/{inproceeding_id}"
)

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
        prev = request.referrer
        return render_template('reference_remove.html',
                        reference=inproceeding,
                        title="Konferenssinjulkaisun artikkelin poisto",
                        conf_message="Haluatko varmasti poistaa tämän artikkelin?",
                        form_url=f"/remove_inproceeding/{inproceeding_id}",
                        remove_button_text="Poista konferenssinjulkaisun artikkeli",
                        prev_url = prev
                        )
    if request.method == 'POST':
        prev_url = request.form.get('prev_url')
        if "remove" in request.form:
            db_helper.delete_inproceeding(inproceeding_id)
            flash('Konferenssijulkaisun artikkeli poistettu onnistuneesti', 'success')
            return redirect('/')
        return redirect(prev_url or '/')

@app.route('/inspect_bibtex')
def inspect_bibtex():
    file = BibtexFile()
    for book in get_books():
        file.add_book(token_hex(5), book)
    for article in get_articles():
        file.add_article(token_hex(5), article)
    for inpro in get_inproceedings():
        file.add_inproceeding(token_hex(5), inpro)


    content = file.get_file_content()

    proxy_file = io.BytesIO(content.encode('utf-8'))

    return send_file(
        proxy_file,
        mimetype='text/x-bibtex',
        as_attachment=False,
        download_name='references.bib'
    )

@app.route('/download_bibtex')
def download_bibtex():
    file = BibtexFile()
    for book in get_books():
        file.add_book(token_hex(5), book)
    for article in get_articles():
        file.add_article(token_hex(5), article)
    for inpro in get_inproceedings():
        file.add_inproceeding(token_hex(5), inpro)


    content = file.get_file_content()

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
