# This file contains the class for the pop up display in the tasks management.
# This file imports the connection to database from another file.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Import the backend class.
from task.task import Task

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
        # Set up the variable to contain the Task class - connection to backend.
        self._data = Task()
        self._taskID = 0 # Variable to store task ID during edit mode.

        # Main layout.
        _mainLayout = QGridLayout()
        self.setLayout(_mainLayout)

        # The pop up area (visible in white.)
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
        self._taskInput.setMaxLength(35)
        self._categoryInput = QComboBox()
        self._categoryInput.setStyleSheet(_dropdownStyle)
        self._categoryInput.setEditable(True)
        self._categoryInput.setToolTip("Category")
        # Calendar inputs.
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
        # Priority input.
        self._priorityInput = QComboBox()
        self._priorityInput.setStyleSheet(_dropdownStyle)
        self._priorityInput.setToolTip("Priority")
        self._priorityInput.addItems(["Low", "Important", "Urgent"])

        # Button panel.
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
        self._actionButton = QPushButton("CREATE", _buttonPanel)
        self._actionButton.setCursor(Qt.PointingHandCursor)
        self._actionButton.clicked.connect(self._create)
        self._actionButton.setStyleSheet("""
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
        _buttonLayout.addWidget(self._actionButton)

        # Adding all the widgets to the visible area.
        _containerLayout.addWidget(self._title, stretch=0)
        _containerLayout.addWidget(self._taskInput, stretch=0)
        _containerLayout.addWidget(self._categoryInput, stretch=0)
        _containerLayout.addWidget(_dateContainer, stretch=0)
        _containerLayout.addWidget(self._priorityInput, stretch=0)
        _containerLayout.addWidget(_buttonPanel, stretch=0)
        
        # Adds the visible area to the rest of the screen.
        _mainLayout.addWidget(self._container)
    
    def _create(self): # Function for creating and updating data.
        _taskName = self._taskInput.text().strip()
        _categoryName = self._categoryInput.currentText().strip()
        _dueDate = self._dueInput.text()
        _executeDate = self._dateInput.text()
        _priority = self._priorityInput.currentText().strip()
        if not _taskName or not _categoryName or not _priority:
            return
        
        if self._taskID > 0:
            self._data.editTask(self._taskID, _categoryName, _taskName, _dueDate, _executeDate, _priority)
        else:
            self._data.createTask(_categoryName, _taskName, _dueDate, _executeDate, _priority)
        self._categoryInput.clear()
        self.hide()

    def resizeEvent(self, event): # Responsive design to window size change.
        self._container.setFixedSize(int(self.width() * 0.65), int(self.height() * 0.40))
    
    def createMode(self): # Sets data ready for create mode.
        self._categoryInput.clear()
        self._categoryInput.addItems([_category[0] for _category in self._data.category()])
        self._title.setText("Create New Task")
        self._title.adjustSize()
        self._title.repaint()
        self._taskInput.setText("")
        self._actionButton.setText("CREATE")
        self._taskID = 0
        self.show()

    def editMode(self, taskID): # Sets data ready for edit mode.
        self._categoryInput.clear()
        self._categoryInput.addItems([_category[0] for _category in self._data.category()])
        self._taskID = taskID
        self._title.setText("Edit Task")
        self._title.adjustSize()
        _taskData = self._data.singleTask(taskID)
        self._taskInput.setText(_taskData[2])
        self._categoryInput.setCurrentText(_taskData[8])
        self._dueInput.setDate(QDate.fromString(_taskData[3]))
        self._dateInput.setDate(QDate.fromString(_taskData[4]))
        self._priorityInput.setCurrentText(_taskData[5])
        self._actionButton.setText("EDIT")
        self.show()
        
class filterTask(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True) # Ensures the Navigation is rendered.
        self.setStyleSheet("""
        background-color: rgba(77, 6, 83, 0.55);
        border-radius: 10px;
        """)

        # Main layout.
        _mainLayout = QGridLayout()
        self.setLayout(_mainLayout)

        # Container for the visible pop up.
        self._container = QWidget(self)
        self._container.setStyleSheet("background-color: white")
        _containerLayout = QVBoxLayout()
        self._container.setLayout(_containerLayout)

        # Title and inputs.
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
        self._dateInput.setDate(QDate.currentDate())
        self._dateInput.setToolTip("Filter by Date")
        _calendar = self._dateInput.calendarWidget()
        _calendar.setStyleSheet(_calendarStyle)
        self._priorityInput = QComboBox()
        self._priorityInput.setStyleSheet(_dropdownStyle)
        self._priorityInput.setToolTip("Filter by Priority")
        # Buttons.
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
        self._filterButton.clicked.connect(lambda: self._updateFilter())
        _buttonLayout.addWidget(self._cancelButton)
        _buttonLayout.addWidget(self._filterButton)

        # Add and position in layout.
        _containerLayout.addWidget(_title, stretch=0)
        _containerLayout.addWidget(self._categoryInput, stretch=0)
        _containerLayout.addWidget(self._dateInput, stretch=0)
        _containerLayout.addWidget(self._priorityInput, stretch=-0)
        _containerLayout.addWidget(_buttonPanel, stretch=0)
        _mainLayout.addWidget(self._container)

        # Predefined variables for usage.
        self._editor = Task()
        self._filterCode = [0, 0, 0]
        self._category = "Null"
        self._date = "Null"
        self._priority = "Null"
    
    def filterMode(self): # Resets the filter pop up.
        self._categoryInput.clear()
        self._categoryInput.addItem("--Select Category--")
        self._categoryInput.setItemData(0, 0, Qt.UserRole - 1)
        _categoryList = self._editor.category()
        self._categoryInput.addItems([_category[0] for _category in _categoryList])
        self._priorityInput.clear()
        self._priorityInput.addItems(["--Select Priority--", "Low", "Important", "Urgent"])
        self._priorityInput.setItemData(0, 0, Qt.UserRole -1)
        self._dateInput.setSpecialValueText("--Select Date--")
        self._dateInput.setDate(self._dateInput.minimumDate())
        self.show()
    
    def _updateFilter(self): # Update the filter data.
        self._category = self._categoryInput.currentText()
        self._date = self._dateInput.text()
        self._priority = self._priorityInput.currentText()
        self._filterCode = [0 if self._category == "--Select Category--" else 1,
                            0 if self._date == "--Select Date--" else 1,
                            0 if self._priority == "--Select Priority--" else 1]
        self.hide()
    
    def filterData(self): # Returns the filter data.
        return ["".join(map(str, self._filterCode)), self._category, self._date, self._priority]

    def resizeEvent(self, event): # Resizes the pop based on window size. 
        self._container.setFixedSize(int(self.width() * 0.65), int(self.height() * 0.35))