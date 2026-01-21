# This file contains the class for the pop up display in the tasks management.
# This file imports the connection to database from another file.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Styling.
_calendarStyle = """
QCalendarWidget QToolButton {
    color: black;
    background-color: transparent;
    font-size: 14px;
    border: none;
}
QCalendarWidget QToolButton::menu-indicator {
    image: none;
}
QCalendarWidget QSpinBox {
    color: black;
    background-color: transparent;
    font-size: 14px;
    border: none;
}
"""
_inputStyle = """
border: 1px solid black;
height: 40px;
font-size: 16px;
padding-left: 10px;
padding-right: 10px;
"""
_dateStyle = f"""
QDateEdit {{
    {_inputStyle}
}}
QDateEdit::drop-down {{
    width: 30px;
    border: none;
}}
QDateEdit::down-arrow {{
    image: url(icon/arrow.png);
    width: 12px;
    height: 12px;
}}"""
_dropdownStyle = f"""
QComboBox {{
    {_inputStyle}
}}
QComboBox::drop-down {{
    width: 30px;
    border: none;
}}
QComboBox::down-arrow {{
    image: url(icon/arrow.png);
    width: 12px;
    height: 12px;
}}
"""

class newTask(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True) # Ensures the Navigation is rendered.
        self.setStyleSheet("""
        background-color: rgba(77, 6, 83, 0.55);
        border-radius: 10px;
        """)

        _mainLayout = QGridLayout()
        self.setLayout(_mainLayout)

        self._container = QWidget(self)
        self._container.setStyleSheet("background-color: white")
        _containerLayout = QVBoxLayout()
        self._container.setLayout(_containerLayout)

        # Inputs
        self._title = QLabel("Create New Task")
        self._title.setStyleSheet("""
        font-size: 25px;
        font-weight: bold;
        """)
        self._taskInput = QLineEdit()
        self._taskInput.setStyleSheet(_inputStyle)
        self._taskInput.setPlaceholderText("Task Name")
        self._taskInput.setToolTip("Task Name")
        self._categoryInput = QComboBox()
        self._categoryInput.setStyleSheet(_dropdownStyle)
        self._categoryInput.setEditable(True)
        self._categoryInput.setToolTip("Category")

        self._dueInput = QDateEdit()
        self._dueInput.setCalendarPopup(True)
        self._dueInput.setDate(QDate.currentDate())
        self._dueInput.setCalendarPopup(True)
        self._dueInput.setStyleSheet(_dateStyle)
        self._dueInput.setToolTip("Due Date")
        _calendar = self._dueInput.calendarWidget()
        _calendar.setStyleSheet(_calendarStyle)
        self._dateInput = QDateEdit()
        self._dateInput.setCalendarPopup(True)
        self._dateInput.setDate(QDate.currentDate())
        self._dateInput.setCalendarPopup(True)
        self._dateInput.setStyleSheet(_dateStyle)
        self._dateInput.setToolTip("Date to Execute Task")
        _calendar = self._dateInput.calendarWidget()
        _calendar.setStyleSheet(_calendarStyle)
        _dateContainer = QWidget(self)
        _dateContainerLayout = QHBoxLayout()
        _dateContainerLayout.setContentsMargins(0, 0, 0, 0)
        _dateContainer.setLayout(_dateContainerLayout)
        _dateContainerLayout.addWidget(self._dueInput)
        _dateContainerLayout.addWidget(self._dateInput)
        
        self._priorityInput = QComboBox()
        self._priorityInput.setStyleSheet(_dropdownStyle)
        self._priorityInput.setToolTip("Priority")

        _buttonPanel = QWidget(self)
        _buttonPanel.setStyleSheet("background-color: white;")
        _buttonLayout = QHBoxLayout()
        _buttonLayout.setContentsMargins(0, 0, 0, 0)
        _buttonPanel.setLayout(_buttonLayout)
        self._cancelButton = QPushButton("CANCEL", _buttonPanel)
        self._cancelButton.setCursor(Qt.PointingHandCursor)
        self._cancelButton.clicked.connect(lambda: self.hide())
        self._cancelButton.setStyleSheet("""
        QPushButton {
            background-color: #DC0000;
            height: 40px;
            font-weight: bold;
            font-size: 14px;
            color: white;
        }
        QPushButton:hover {
            background-color: #6D0000;
        }
        """)
        self._createButton = QPushButton("CREATE", _buttonPanel)
        self._createButton.setCursor(Qt.PointingHandCursor)
        self._createButton.setStyleSheet("""
        QPushButton {
            background-color: #009687;
            height: 40px;
            font-weight: bold;
            font-size: 14px;
            color: white;
        }
        QPushButton:hover {
            background-color: #00524A;
        }
        """)
        _buttonLayout.addWidget(self._cancelButton)
        _buttonLayout.addWidget(self._createButton)

        _containerLayout.addWidget(self._title, stretch=0)
        _containerLayout.addWidget(self._taskInput, stretch=0)
        _containerLayout.addWidget(self._categoryInput, stretch=0)
        _containerLayout.addWidget(_dateContainer, stretch=0)
        _containerLayout.addWidget(self._priorityInput, stretch=0)
        _containerLayout.addWidget(_buttonPanel, stretch=0)
        
        _mainLayout.addWidget(self._container)
    
    def resizeEvent(self, event):
        self._container.setFixedSize(int(self.width() * 0.65), int(self.height() * 0.40))

class filterTask(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True) # Ensures the Navigation is rendered.
        self.setStyleSheet("""
        background-color: rgba(77, 6, 83, 0.55);
        border-radius: 10px;
        """)

        _mainLayout = QGridLayout()
        self.setLayout(_mainLayout)

        self._container = QWidget(self)
        self._container.setStyleSheet("background-color: white")
        _containerLayout = QVBoxLayout()
        self._container.setLayout(_containerLayout)

        _title = QLabel("Filter")
        _title.setStyleSheet("""
        font-size: 25px;
        font-weight: bold;
        """)
        self._categoryInput = QComboBox()
        self._categoryInput.setStyleSheet(_dropdownStyle)
        self._categoryInput.setToolTip("Filter by Category")
        self._dateInput = QDateEdit()
        self._dateInput.setCalendarPopup(True)
        self._dateInput.setStyleSheet(_dateStyle)
        self._dateInput.setToolTip("Filter by Date")
        _calendar = self._dateInput.calendarWidget()
        _calendar.setStyleSheet(_calendarStyle)
        self._priorityInput = QComboBox()
        self._priorityInput.setStyleSheet(_dropdownStyle)
        self._priorityInput.setToolTip("Filter by Priority")

        _buttonPanel = QWidget(self)
        _buttonPanel.setStyleSheet("background-color: white")
        _buttonLayout = QHBoxLayout()
        _buttonLayout.setContentsMargins(0, 0, 0, 0)
        _buttonPanel.setLayout(_buttonLayout)
        self._cancelButton = QPushButton("CANCEL", _buttonPanel)
        self._cancelButton.setCursor(Qt.PointingHandCursor)
        self._cancelButton.clicked.connect(lambda: self.hide())
        self._cancelButton.setStyleSheet("""
        QPushButton {
            background-color: #DC0000;
            height: 40px;
            font-weight: bold;
            font-size: 14px;
            color: white;
        }
        QPushButton:hover {
            background-color: #6D0000;
        }
        """)
        self._filterButton = QPushButton("FILTER", _buttonPanel)
        self._filterButton.setCursor(Qt.PointingHandCursor)
        self._filterButton.setStyleSheet("""
        QPushButton {
            background-color: #009687;
            height: 40px;
            font-weight: bold;
            font-size: 14px;
            color: white;
        }
        QPushButton:hover {
            background-color: #00524A;
        }
        """)
        _buttonLayout.addWidget(self._cancelButton)
        _buttonLayout.addWidget(self._filterButton)

        _containerLayout.addWidget(_title, stretch=0)
        _containerLayout.addWidget(self._categoryInput, stretch=0)
        _containerLayout.addWidget(self._dateInput, stretch=0)
        _containerLayout.addWidget(self._priorityInput, stretch=-0)
        _containerLayout.addWidget(_buttonPanel, stretch=0)

        _mainLayout.addWidget(self._container)
    
    def resizeEvent(self, event):
        self._container.setFixedSize(int(self.width() * 0.65), int(self.height() * 0.35))