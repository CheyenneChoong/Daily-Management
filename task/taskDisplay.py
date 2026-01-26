# This file contains the class that focuses on the display of data and information.
# Data handling is done in a different file.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from task.taskPopup import *
from task.task import Task

class mainTask(QWidget) :
    def __init__(self): # Constructor function.
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True) # Ensures the Navigation is rendered.
        self.setStyleSheet("""
        background-color: rgba(209, 187, 255, 0.6);
        border-radius: 10px;
        """)
        self._editor = Task()

        # Set up the main layout.
        _layout1 = QVBoxLayout()
        _layout1.setContentsMargins(25, 25, 25, 25)
        _layout1.setSpacing(15)
        self.setLayout(_layout1)

        # Title Panel.
        _title = QLabel("Tasks", self)
        _title.setStyleSheet("""
        background-color: none;
        font-size: 25px;
        color: white;
        font-weight: bold;
        """)
        _title.adjustSize()

        # Top Panel - Create Button and Search Bar Row.
        _topPanel = QWidget(self)
        _layout2 = QHBoxLayout()
        _layout2.setContentsMargins(0, 0, 0, 0)
        _topPanel.setLayout(_layout2)
        _topPanel.setStyleSheet("background-color: none;")
        _style = """
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
        """
        self._createButton = QPushButton("CREATE", _topPanel)
        self._createButton.setStyleSheet(_style)
        self._createButton.setCursor(Qt.PointingHandCursor)
        self._filterButton = QPushButton("FILTER", _topPanel)
        self._filterButton.setStyleSheet(_style)
        self._filterButton.setCursor(Qt.PointingHandCursor)
        _layout2.addWidget(self._createButton)
        _layout2.addWidget(self._filterButton)

        # Main content area where tasks are displayed.
        self._contentArea = QWidget(self)
        self._contentArea.setStyleSheet("background-color: transparent")
        self._layout4 = QVBoxLayout()
        self._layout4.setAlignment(Qt.AlignTop)
        self._layout4.setContentsMargins(0, 0, 0, 0)
        self._contentArea.setLayout(self._layout4)
        _scroll = QScrollArea()
        _scroll.setWidgetResizable(True)
        _scroll.setWidget(self._contentArea)
        _scroll.setStyleSheet("""
        QScrollArea {
            background-color: transparent;
        } 
        QScrollBar:vertical { 
            background: black; 
            width: 4px; 
        }
        """)
        self._displayTask(self._editor.filterTask(["000", None, None, None]))

        # Adding all the widgets into the layout.
        _layout1.addWidget(_title, stretch=0)
        _layout1.addWidget(_topPanel, stretch=0)
        _layout1.addWidget(_scroll, stretch=1)
        _layout1.activate()

        # New Task / Edit Task Pop Up
        self._newTaskPopUp = newTask(self)
        self._newTaskPopUp.hide()
        self._newTaskPopUp.installEventFilter(self)
        self._createButton.clicked.connect(lambda: self._newTaskPopUp.createMode())

        # Filter Task Pop Up
        self._filterTaskPopUp = filterTask(self)
        self._filterTaskPopUp.hide()
        self._filterTaskPopUp.installEventFilter(self)
        self._filterButton.clicked.connect(lambda: self._filterTaskPopUp.filterMode())

    def resizeEvent(self, event): # Resizes the pop up according to the window size.
        self._newTaskPopUp.setGeometry(self.rect())
        self._filterTaskPopUp.setGeometry(self.rect())

    def eventFilter(self, component, event): # Calls the refresh data function every time a pop up is closed.
        if event.type() == QEvent.Hide:
            self._refreshData()
        return super().eventFilter(component, event)
    
    def _refreshData(self): # Refreshes the data.
        while self._layout4.count():
            _data = self._layout4.takeAt(0)
            _widget = _data.widget()
            _widget.deleteLater()
        _filter = self._filterTaskPopUp.filterData()
        self._displayTask(self._editor.filterTask(_filter))
        
    def _displayTask(self, data): # Displays the data.
        _allTask = data
        for _data in _allTask:
            _task = QWidget(self._contentArea)
            _task.setMaximumHeight(65)
            _task.setStyleSheet("background-color: white")
            _taskLayout = QHBoxLayout()
            _taskLayout.setContentsMargins(25, 0, 25, 0)
            _task.setLayout(_taskLayout)

            _check = QCheckBox(_task)
            _check.setCheckState(Qt.Checked if _data[7] == "completed" else Qt.Unchecked)
            _check.setStyleSheet("""
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid black;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid black;
                background-color: #4B0096
            }
            """)
            _check.clicked.connect(lambda checked, taskID = _data[0]: self._editor.markTask(taskID, QDate.currentDate().toString("M/d/yyyy")))
            _taskLayout.addWidget(_check, stretch=0)

            _detail = QWidget(_task)
            _detailLayout = QVBoxLayout()
            _detail.setLayout(_detailLayout)
            _taskName = QLabel(_data[2], _task)
            _taskName.setStyleSheet("font-weight: bold; font-size: 18px")
            _taskDetail = QLabel(f"{_data[8]}, Due Date: {_data[3]}")
            _taskDetail.setStyleSheet("font-size: 12px")
            _detailLayout.addWidget(_taskName)
            _detailLayout.addWidget(_taskDetail)
            _taskLayout.addWidget(_detail, stretch=1)

            _priority = QLabel(_data[5], _task)
            _priority.setStyleSheet(f"""
            background-color: {"#DBA9FF" if _data[5] == "Low" else "#FEFFA9" if _data[5] == "Important" else "#FF9193" };
            font-weight: bold;
            font-size: 14px;
            """)
            _priority.setMaximumSize(150, 40)
            _priority.setAlignment(Qt.AlignCenter)
            _taskLayout.addWidget(_priority, stretch=1)

            _button = QWidget(_task)
            _buttonLayout = QHBoxLayout()
            _button.setLayout(_buttonLayout)
            _editButton = QPushButton(_button)
            _editButton.setIcon(QIcon("icon/edit.png"))
            _editButton.setIconSize(QSize(25, 25))
            _editButton.clicked.connect(lambda event, taskID = _data[0]: self._newTaskPopUp.editMode(taskID))
            _deleteButton = QPushButton(_button)
            _deleteButton.setIcon(QIcon("icon/delete.png"))
            _deleteButton.setIconSize(QSize(25, 25))
            _deleteButton.clicked.connect(lambda event, taskID = _data[0]: (self._editor.deleteTask(taskID), self._refreshData()))
            _buttonLayout.addWidget(_editButton, stretch=0)
            _buttonLayout.addWidget(_deleteButton, stretch=0)
            _taskLayout.addWidget(_button, stretch=0)
            self._layout4.addWidget(_task, stretch=0)
