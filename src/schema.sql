CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    title TEXT,
    writer TEXT,
    year TEXT,
    isbn TEXT,
    user_id INTEGER REFERENCES users
);
