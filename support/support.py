# This file handles the data management and connection to the database for this feature.
# Import library for SQL.
import sqlite3

class emotionalState():
    def create(self, emotionInput):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"INSERT INTO emotion (emotionalState) VALUES ('{emotionInput}');")
        _connect.commit()
        _connect.close()
    
    def edit(self, emotionID, emotionInput):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"UPDATE emotion SET emotionalState = '{emotionInput}' WHERE emotionID = {emotionID};")
        _connect.commit()
        _connect.close()
    
    def delete(self, emotionID):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"DELETE FROM emotion WHERE emotionID = {emotionID};")
        _connect.commit()
        _connect.close()

    def emotion(self):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _data = _cursor.execute("SELECT * FROM emotion;")
        _data = _data.fetchall()
        _connect.commit()
        _connect.close()
        return _data

    def singleEmotion(self, emotionID):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _data = _cursor.execute(f"SELECT * FROM emotion WHERE emotionID = {emotionID};")
        _data = _data.fetchone()
        _connect.commit()
        _connect.close()
        return _data