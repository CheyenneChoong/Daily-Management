"""
The code in this file focuses on ensuring the existance
of the database and all its table. 
"""

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
_cursor.execute("""
CREATE TABLE IF NOT EXISTS support (
    supportID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    link TEXT NOT NULL
)
""")
_cursor.execute("""
CREATE TABLE IF NOT EXISTS emotion (
    emotionID INTEGER PRIMARY KEY AUTOINCREMENT,
    emotionalState TEXT NOT NULL
)
""")
_cursor.execute("""
CREATE TABLE IF NOT EXISTS schedule (
    scheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT NOT NULL,
    dateTime TEXT,
    venue TEXT
)
""")
_cursor.execute("""
CREATE TABLE IF NOT EXISTS emotionalSupport (
    emotionalSupportID INTEGER PRIMARY KEY AUTOINCREMENT,
    supportID INTEGER,
    emotionID INTEGER,
    FOREIGN KEY (supportID) REFERENCES support(supportID) ON DELETE CASCADE,
    FOREIGN KEY (emotionID) REFERENCES emotion(emotionID) ON DELETE CASCADE
)
""")
_cursor.execute("""
CREATE TABLE IF NOT EXISTS scheduleState (
    scheduleStateID INTEGER PRIMARY KEY AUTOINCREMENT,
    scheduleID INTEGER,
    emotionID INTEGER,
    FOREIGN KEY (scheduleID) REFERENCES schedule(scheduleID) ON DELETE CASCADE,
    FOREIGN KEY (emotionID) REFERENCES emotion(emotionID) ON DELETE CASCADE
)
""")
_connect.commit()
_connect.close()