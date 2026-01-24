# Code for setting up the database file if it doesn't exists.
# Code also ensures the tables are created.
import sqlite3

_connect = sqlite3.connect("data/database.db")
_cursor = _connect.cursor()
_cursor.execute("PRAGMA foreign_keys = ON;")
_cursor.execute("""
CREATE TABLE IF NOT EXISTS category (
    categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    categoryName TEXT NOT NULL 
);""")
_cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    taskID INTEGER PRIMARY KEY AUTOINCREMENT,
    categoryID INTEGER,
    taskName TEXT NOT NULL,
    dueDate TEXT NOT NULL,
    executeDate TEXT NOT NULL,
    priority TEXT NOT NULL,
    completionDate TEXT,
    status TEXT NOT NULL,
    FOREIGN KEY (categoryID) REFERENCES category(categoryID) ON DELETE CASCADE
)
""")
_connect.commit()
_connect.close()