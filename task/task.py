import sqlite3

class Task():
    """
    :func createTask: Add new task.
    :func editTask: Edit a selected task.
    :func markTask: Marks a task as done or pending.
    :func deleteTask: Deletes a selected task.
    :func _deleteCategory: Checks if the category is needed and deletes if there is no need for the category.
    :func filterTask: Retrieves information of tasks after appylying filters (if applicable)
    :func singleTask: Retrieves information of a single task.
    :func category: Retrieves all the categories.
    """

    def createTask(self, categoryName, taskName, dueDate, executeDate, priority):
        """
        :param categoryName: Name of the category the task is categorized in.
        :param taskName: Name of the task.
        :param dueDate: Deadline for the task.
        :param executeDate: Date when the task should be done.
        :param priority: Priority of the task.
        """
        categoryName = categoryName.replace("'", "''")
        taskName = taskName.replace("'", "''")
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
        """
        :param taskID: ID of the task being edited.
        :param categoryName: Name of the category the task is categorized in.
        :param taskName: Name of the task.
        :param dueDate: Deadline for the task.
        :param executeDate: Date when the task should be done.
        :param priority: Priority of the task.
        """
        categoryName = categoryName.replace("'", "''")
        taskName = taskName.replace("'", "''")

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
        """
        :param taskID: ID of task being edited.
        :param date: Date of when the task was marked.
        """
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
        """
        :param taskID: ID of the task being deleted.
        """
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
    
    def filterTask(self, filterCode):
        """
        :param filterCode: List of the filter code and the filter parameters.
        The filter code is a 3 digit code to filter based on priority, executeDate
        and categoryName. 
        """
        _filter = {"category": f"c.categoryName = '{filterCode[1]}'", 
                   "date": f"t.executeDate = '{filterCode[2]}'", 
                   "priority": f"t.priority = '{filterCode[3]}'"}
        _filterCombination = {
            "000" : "",
            "001" : f"WHERE {_filter['priority']}",
            "010" : f"WHERE {_filter['date']}",
            "100" : f"WHERE {_filter['category']}",
            "011" : f"WHERE {_filter['date']} AND {_filter['priority']}",
            "101" : f"WHERE {_filter['category']} AND {_filter['priority']}",
            "110" : f"WHERE {_filter['category']} AND {_filter['date']}",
            "111" : f"WHERE {_filter['category']} AND {_filter['date']} AND {_filter['priority']}"
        }

        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")
        _sql = _cursor.execute(f"""
        SELECT t.*, c.categoryName
        FROM tasks t LEFT JOIN category c ON t.categoryID = c.categoryID
        {_filterCombination[filterCode[0]]};
        """)
        _data = _sql.fetchall()
        _connect.commit()
        _connect.close()
        return _data

    def singleTask(self, taskID):
        """
        :param taskID: ID of the task being selected.
        """
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