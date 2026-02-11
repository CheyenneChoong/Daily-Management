from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3

class taskSummary(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        background-color: #C9ADFF;
        border-radius: 10px;
        """)

        _mainLayout = QVBoxLayout()
        _mainLayout.setContentsMargins(15, 15, 15, 15)
        _mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(_mainLayout)

        _topPanel = QWidget()
        _topPanel.setStyleSheet("background-color: none;")
        _topPanelLayout = QHBoxLayout()
        _topPanelLayout.setContentsMargins(0, 0, 0, 0)
        _topPanel.setLayout(_topPanelLayout)
        _title = QLabel("Task Progress", _topPanel)
        _title.setStyleSheet("""
        background-color: none;
        font-size: 20px;
        color: black;
        font-weight: bold;
        """)
        _title.adjustSize()
        _refreshButton = QPushButton("REFRESH", _topPanel)
        _refreshButton.setStyleSheet("""
        QPushButton {
            background-color: #4B0096;
            color: white;
            font-weight: bold;
            padding-left: 20px;
            padding-right: 20px;
            height: 40px;
        }
        QPushButton:hover {
            background-color: #321153;
        }
        """)
        _refreshButton.clicked.connect(self._refreshData)
        _refreshButton.setCursor(Qt.PointingHandCursor)
        _topPanelLayout.addWidget(_title, stretch = 1)
        _topPanelLayout.addWidget(_refreshButton, stretch = 0)

        self._container = QWidget(self)
        self._container.setStyleSheet("background-color: none;")
        self._containerLayout = QVBoxLayout()
        self._containerLayout.setContentsMargins(0, 0, 0, 0)
        self._containerLayout.setAlignment(Qt.AlignTop)
        self._container.setLayout(self._containerLayout)
        _scroll = QScrollArea()
        _scroll.setWidgetResizable(True)
        _scroll.setWidget(self._container)
        _scroll.setStyleSheet("""
        QScrollArea {
            background-color: transparent;
        } 
        QScrollBar:vertical { 
            background: black; 
            width: 4px; 
        }
        """)

        self._refreshData()

        _mainLayout.addWidget(_topPanel, stretch = 0)
        _mainLayout.addWidget(_scroll, stretch = 1)

    def _refreshData(self):
        """
        Function used to refresh the data being displayed. The data displayed
        is the progress of the tasks completed by category. The function 
        removes the old data before displaying the latest data. This ensures
        the data displayed is accurate and timely.
        """
        while self._containerLayout.count():
            _widget = self._containerLayout.takeAt(0)
            _widget = _widget.widget()
            _widget.deleteLater()
        
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _cursor.execute("PRAGMA foreign_keys = ON;")

        _allCategory = _cursor.execute("SELECT * FROM category;")
        _allCategory = _allCategory.fetchall()
        for _category in _allCategory:
            _status = _cursor.execute(f"""SELECT SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed,
                                      SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending 
                                      FROM tasks WHERE categoryID = {_category[0]};""")
            _status = _status.fetchone()
            _widget = QWidget(self._container)
            
            _widget.setStyleSheet("background-color: white;")
            _widgetLayout = QHBoxLayout()
            _widgetLayout.setContentsMargins(25, 15, 25, 15)
            _widget.setLayout(_widgetLayout)

            _categoryName = QLabel(_category[1], _widget)
            _categoryName.setStyleSheet("font-weight: bold; font-size: 16px")
            _calculate = int(_status[0] / (_status[0] + _status[1]) * 100)
            _progress = QLabel(str(f"{_calculate}%"), _widget)
            _progress.setStyleSheet(f"""
            background-color: {"#FFA9A9" if _calculate < 25 else "#DBA9FF" if _calculate >= 25 and _calculate < 80 else "#A9FFBC"};
            font-weight: bold;
            font-size: 14px;
            padding: 10px;
            """)
            _progress.setMaximumSize(100, 40)
            _progress.setAlignment(Qt.AlignCenter)
            
            _widgetLayout.addWidget(_categoryName)
            _widgetLayout.addWidget(_progress)
            self._containerLayout.addWidget(_widget)

        _connect.commit()
        _connect.close()