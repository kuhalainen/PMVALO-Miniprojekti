CREATE TABLE users (
<<<<<<< HEAD
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE items (
=======
>>>>>>> ff87799 (etusivulla näkyy lisätyt kirjat)
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    title TEXT,
    writer TEXT,
    year TEXT,
    isbn TEXT,
<<<<<<< HEAD
=======
    publisher TEXT,
>>>>>>> ff87799 (etusivulla näkyy lisätyt kirjat)
    user_id INTEGER REFERENCES users(id) 
);