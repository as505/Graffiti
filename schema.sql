DROP TABLE IF EXISTS idTable;
DROP TABLE IF EXISTS users;

CREATE TABLE idTable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token VARCHAR(255)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    last_action_ts timestamp
);
