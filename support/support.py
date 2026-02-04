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

class support():
    def create(self, name, link, emotionalState):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"INSERT INTO support (name, link) VALUES ('{name}', '{link}');")
        _supportID = _cursor.lastrowid
        for _emotionID in emotionalState:
            _cursor.execute(f"INSERT INTO emotionalSupport (supportID, emotionID) VALUES ({_supportID}, {_emotionID});")
        _connect.commit()
        _connect.close()
    
    def edit(self, supportID, name, link, emotionalState):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"UPDATE support SET name = '{name}', link = '{link}' WHERE supportID = {supportID};")
        
        _allCurrent = _cursor.execute(f"SELECT emotionalSupportID, emotionID FROM emotionalSupport WHERE supportID = {supportID};")
        _allCurrent = _allCurrent.fetchall()
        for _current in _allCurrent:
            if _current[1] not in emotionalState:
                _cursor.execute(f"DELETE FROM emotionalSupport WHERE emotionalSupportID = {_current[0]};")
            elif _current[1] in emotionalState:
                emotionalState.remove(_current[1])
        
        for _emotionID in emotionalState:
            _cursor.execute(f"INSERT INTO emotionalSupport (supportID, emotionID) VALUES ({supportID}, {_emotionID});")

        _connect.commit()
        _connect.close()
    
    def delete(self, supportID):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"DELETE FROM support WHERE supportID = {supportID};")
        _connect.commit()
        _connect.close()

    def allSupport(self):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _supportData = _cursor.execute("SELECT * FROM support;")
        _supportData = _supportData.fetchmany()
        _connect.commit()
        _connect.close()
        return _supportData
    
    def singleSupport(self, supportID):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _supportData = _cursor.execute(f"SELECT * FROM support WHERE supportID = {supportID};")
        _supportData = _supportData.fetchone()
        _connect.commit()
        _connect.close()
        return _supportData

    def emotions(self, supportID):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _emotions = _cursor.execute(f"""SELECT e.emotionID FROM emotionalSupport s 
                                    LEFT JOIN emotion e ON s.emotionID = e.emotionID
                                    WHERE s.supportID = {supportID}""")
        _emotions = _emotions.fetchall()
        _connect.commit()
        _connect.close()
        return [_emotion[0] for _emotion in _emotions]