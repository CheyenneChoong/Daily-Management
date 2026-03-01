import sqlite3

"""
emotionalState: Used for CRUD related to the emotion table.
support: Used for CRUD related to the supports and the emotions its tied to.
"""

class emotionalState():
    """
    :func create: Adds a new emotional state.
        :param emotionInput: Name of the emotional state. Example: Happy
    :func edit: Edits the emotional state.
        :param emotionID: ID of the emotional state being edited.
        :param emotionInput: Name of the emotional state.
    :func delete: Deletes an emotional state.
        :param emotionID: ID of the emotional state being deleted.
    :func emotion: Retrieves information of all emotional state in the database.
    :func singleEmotion: Retrieves information of an emotional state that is being selected.
        :param emotionID: ID of the emotional state being selected.
    """
    def create(self, emotionInput):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"INSERT INTO emotion (emotionalState) VALUES ('{emotionInput.replace("'", "''")}');")
        _connect.commit()
        _connect.close()
    
    def edit(self, emotionID, emotionInput):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"UPDATE emotion SET emotionalState = '{emotionInput.replace("'", "''")}' WHERE emotionID = {emotionID};")
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
    """
    :func create: Add support and link it with the emotional state.
    :func edit: Edit the support.
    :func delete: Delete the support.
    :func allSupport: Retrieves information of all the support.
    :func singleSupport: Retrieves information of a selected support.
    :func emotions: Retrieves the emotionIDs linked to a support.
    """
    def create(self, name, link, emotionalState):
        """
        :param name: Name of the support. Example: Run Music Video
        :param link: Link to the support. Example: YouTube link, PDF link
        :param emotionalState: List of emotionIDs connected to the support.
        """
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"INSERT INTO support (name, link) VALUES ('{name.replace("'", "''")}', '{link}');")
        _supportID = _cursor.lastrowid
        for _emotionID in emotionalState:
            _cursor.execute(f"INSERT INTO emotionalSupport (supportID, emotionID) VALUES ({_supportID}, {_emotionID});")
        _connect.commit()
        _connect.close()
    
    def edit(self, supportID, name, link, emotionalState):
        """
        :param supportID: ID of the selected support to be edited.
        :param name: Name of the support. Example: Run Music Video
        :param link: Link to the support. Example: YouTube link, PDF link
        :param emotionalState: List of emotionIDs connected to the support.
        """
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"UPDATE support SET name = '{name.replace("'", "''")}', link = '{link}' WHERE supportID = {supportID};")
        
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
        """
        :param supportID: ID of the support being deleted.
        """
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
        _supportData = _supportData.fetchall()
        _connect.commit()
        _connect.close()
        return _supportData
    
    def singleSupport(self, supportID):
        """
        :param supportID: ID of the support being selected.
        """
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _supportData = _cursor.execute(f"SELECT * FROM support WHERE supportID = {supportID};")
        _supportData = _supportData.fetchone()
        _connect.commit()
        _connect.close()
        return _supportData

    def emotions(self, supportID):
        """
        :param supportID: ID of the support being selected.
        """
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _emotions = _cursor.execute(f"SELECT emotionID FROM emotionalSupport WHERE supportID = {supportID}")
        _emotions = _emotions.fetchall()
        _connect.commit()
        _connect.close()
        return [_emotion[0] for _emotion in _emotions]