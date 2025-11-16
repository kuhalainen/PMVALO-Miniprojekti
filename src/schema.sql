CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    writer TEXT,
    year TEXT,
    isbn TEXT,
    user_id INTEGER REFERENCES users
);
