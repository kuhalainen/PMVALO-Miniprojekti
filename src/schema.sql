CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT,
    writer TEXT,
    year TEXT,
    isbn TEXT,
    publisher TEXT,
    user_id INTEGER REFERENCES users(id) 
);

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    writer TEXT,
    year TEXT,
    DOI TEXT,
    journal TEXT,
    volume TEXT,
    pages TEXT
);

CREATE TABLE inproceedings (
    id SERIAL PRIMARY KEY,
    title TEXT,
    writer TEXT,
    year TEXT,
    booktitle TEXT
);