import sqlite3

"""
Schedule class is created for data handling and connection to database.
This covers the basic CRUD system. 

:func create: Adds a new event.
:func edit: Edit an existing event.
:func delete: Deletes an existing event.
:func getSchedule: Retrieves all the events after filtering (if applicable).
:func singleSchedule: Retrieves data for a single event.
:func emotions: Retrieves the emotionIDs connected to an event.
"""

class schedule():
    def create(self, event, dateTime, venue, emotionalState):
        """
        :param event: Name / title of the event.
        :param dateTime: The date and time of the scheduled event.
        :param venue: Location of the event.
        :param emotionalState: List of all emotionIDs connected to the event.
        """
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"INSERT INTO schedule (event, dateTime, venue) VALUES ('{event.replace("'", "''")}', '{dateTime}', '{venue.replace("'", "''")}');")
        _scheduleID = _cursor.lastrowid
        for _emotion in emotionalState:
            _cursor.execute(f"INSERT INTO scheduleState (scheduleID, emotionID) VALUES ({_scheduleID}, {_emotion});")
        _connect.commit()
        _connect.close()
    
    def edit(self, scheduleID, event, dateTime, venue, emotionalState):
        """
        :param scheduleID: ID of the event that is being edited.
        :param event: Name / title of the event.
        :param dateTime: The date and time of the scheduled event.
        :param venue: Location of the event.
        :param emotionalState: List of all emotionIDs connected to the event.
        """
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"""UPDATE schedule 
                        SET event = '{event.replace("'", "''")}', dateTime = '{dateTime}', venue = '{venue.replace("'", "''")}'
                        WHERE scheduleID = {scheduleID}""")
        
        _allCurrent = _cursor.execute(f"SELECT scheduleStateID, emotionID FROM scheduleState WHERE scheduleID = {scheduleID};")
        _allCurrent = _allCurrent.fetchall()
        for _current in _allCurrent:
            if _current[1] not in emotionalState:
                _cursor.execute(f"DELETE FROM scheduleState WHERE scheduleStateID = {_current[0]};")
            elif _current[1] in emotionalState:
                emotionalState.remove(_current[1])
        
        for _emotionID in emotionalState:
            _cursor.execute(f"INSERT INTO scheduleState (scheduleID, emotionID) VALUES ({scheduleID}, {_emotionID});")

        with open("data/log.txt", "r") as _file:
            _current = _file.readlines()
        
        with open("data/log.txt", "w") as _file:
            for _line in _current:
                if f"S{scheduleID}" not in _line.split("|")[0]:
                    _file.write(_line)

        _connect.commit()
        _connect.close()
    
    def delete(self, scheduleID):
        """
        :param scheduleID: ID of the event that is going to be deleted.
        """
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"DELETE FROM schedule WHERE scheduleID = {scheduleID};")
        _connect.commit()
        _connect.close()
    
    def getSchedule(self, filter):
        """
        :param filter: Filter condition - search input / date.
        """
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()

        if filter:
            filter = filter.replace("'", "''")
            _scheduleData = _cursor.execute(f"""SELECT * FROM schedule WHERE event LIKE '%{filter}%' OR dateTime LIKE '%{filter}%' OR venue LIKE '%{filter}%';""")
        else:
            _scheduleData = _cursor.execute("SELECT * FROM schedule;")
        _scheduleData = _scheduleData.fetchall()
        _connect.commit()
        _connect.close()
        return _scheduleData

    def singleSchedule(self, scheduleID):
        """
        :param scheduleID: ID of the event being selected.
        """
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _scheduleData = _cursor.execute(f"SELECT * FROM schedule WHERE scheduleID = {scheduleID};")
        _scheduleData = _scheduleData.fetchone()
        _connect.commit()
        _connect.close()
        return _scheduleData

    def emotions(self, scheduleID):
        """
        :param scheduleID: ID of the event being selected.
        """
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _scheduleEmotion = _cursor.execute(f"SELECT emotionID FROM scheduleState WHERE scheduleID = {scheduleID};")
        _scheduleEmotion = _scheduleEmotion.fetchall()
        _connect.commit()
        _connect.close()
        return [_emotion[0] for _emotion in _scheduleEmotion]