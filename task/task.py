# Import database module.
import sqlite3

class Task():
    def createTask(self, categoryName, taskName, dueDate, executeDate, priority):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _categoryCheck = _cursor.execute(f"SELECT categoryID FROM category WHERE categoryName = '{categoryName}';")
        _categoryID = _categoryCheck.fetchone()
        if not _categoryID:
            _cursor.execute(f"INSERT INTO category (categoryName) VALUES ('{categoryName}');")
            _categoryID = _cursor.lastrowid
        else:
            _categoryID = _categoryID[0]
        _cursor.execute(f"""
        INSERT INTO tasks (categoryID, taskName, dueDate, executeDate, priority, completionDate, status)
        VALUES ({_categoryID}, '{taskName}', '{dueDate}', '{executeDate}', '{priority}', NULL, 'pending');
        """)
        _connect.commit()
        _connect.close()
    
    def editTask(self, taskID, categoryName, taskName, dueDate, executeDate, priority):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")

        _categoryCheck = _cursor.execute(f"SELECT categoryID FROM category WHERE categoryName = '{categoryName}';")
        _categoryID = _categoryCheck.fetchone()
        if not _categoryID:
            _cursor.execute(f"INSERT INTO category (categoryName) VALUES ('{categoryName}');")
            _categoryID = _cursor.lastrowid
        else:
            _categoryID = _categoryID[0]
        
        _cursor.execute(f"""
        UPDATE tasks SET
        categoryID = '{_categoryID}',
        taskName = '{taskName}',
        dueDate = '{dueDate}',
        executeDate = '{executeDate}',
        priority = '{priority}'
        WHERE taskID = '{taskID}';
        """)

        _connect.commit()
        _connect.close()
        self._deleteCategory()
    
    def markTask(self, taskID, date):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")

        _checkStatus = _cursor.execute(f"SELECT status FROM tasks WHERE taskID = '{taskID}';")
        _status = _checkStatus.fetchone()[0]
        if _status == "pending":
            _cursor.execute(f"UPDATE tasks SET status = 'completed', completionDate = '{date}' WHERE taskID = '{taskID}';")
        else:
            _cursor.execute(f"UPDATE tasks SET status = 'pending', completionDate = NULL WHERE taskID = '{taskID}';")

        _connect.commit()
        _connect.close()
        self._deleteCategory()
    
    def deleteTask(self, taskID):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _cursor.execute(f"DELETE FROM tasks WHERE taskID = {taskID};")
        _connect.commit()
        _connect.close()
        self._deleteCategory()
    
    def _deleteCategory(self):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")

        _cursor.execute("""
        DELETE FROM category
        WHERE categoryID NOT IN (SELECT DISTINCT categoryID FROM tasks);
        """)

        _connect.commit()
        _connect.close()
    
    def allTask(self):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _sql = _cursor.execute(f"""
        SELECT t.*, c.categoryName
        FROM tasks t LEFT JOIN category c ON t.categoryID = c.categoryID;
        """)
        _data = _sql.fetchall()
        _connect.commit()
        _connect.close()
        return _data

    def singleTask(self, taskID):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _sql = _cursor.execute(f"""
        SELECT t.*, c.categoryName
        FROM tasks t LEFT JOIN category c ON t.categoryID = c.categoryID
        WHERE t.taskID = '{taskID}';
        """)
        _data = _sql.fetchone()
        _connect.commit()
        _connect.close()
        return _data

    def category(self):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _sql = _cursor.execute("SELECT categoryName FROM category")
        _data = _sql.fetchall()
        _connect.commit()
        _connect.close()
        return _data