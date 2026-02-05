# The file contains the code for data handling for schedule.
# Import sqlite3.
import sqlite3

class schedule():
    def create(self, event, dateTime, venue, emotionalState):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"INSERT INTO schedule (event, dateTime, venue) VALUES ('{event}', '{dateTime}', '{venue}');")
        _scheduleID = _cursor.lastrowid
        for _emotion in emotionalState:
            _cursor.execute(f"INSERT INTO scheduleState (scheduleID, emotionID) VALUES ({_scheduleID}, {_emotion});")
        _connect.commit()
        _connect.close()
    
    def edit(self, scheduleID, event, dateTime, venue, emotionalState):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"""UPDATE schedule 
                        SET event = '{event}', dateTime = '{dateTime}', venue = '{venue}'
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

        _connect.commit()
        _connect.close()
    
    def delete(self, scheduleID):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"DELETE FROM schedule WHERE scheduleID = {scheduleID};")
        _connect.commit()
        _connect.close()
    
    def getSchedule(self, filter):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()

        if filter:  
            _scheduleData = _cursor.execute(f"""SELECT * FROM schedule WHERE event LIKE '%{filter}%' OR dateTime LIKE '%{filter}%' OR venue LIKE '%{filter}%';""")
        else:
            _scheduleData = _cursor.execute("SELECT * FROM schedule;")
        _scheduleData = _scheduleData.fetchall()
        _connect.commit()
        _connect.close()
        return _scheduleData

    def singleSchedule(self, scheduleID):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _scheduleData = _cursor.execute(f"SELECT * FROM schedule WHERE scheduleID = {scheduleID};")
        _scheduleData = _scheduleData.fetchone()
        _connect.commit()
        _connect.close()
        return _scheduleData

    def emotions(self, scheduleID):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _scheduleEmotion = _cursor.execute(f"SELECT emotionID FROM scheduleState WHERE scheduleID = {scheduleID};")
        _scheduleEmotion = _scheduleEmotion.fetchall()
        _connect.commit()
        _connect.close()
        return [_emotion[0] for _emotion in _scheduleEmotion]