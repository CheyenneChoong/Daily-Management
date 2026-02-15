from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from task.taskPopup import *
from task.task import Task

class mainTask(QWidget) :
    def __init__(self): 
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        background-color: rgba(209, 187, 255, 0.6);
        border-radius: 10px;
        """)
        self._editor = Task()

        _mainLayout = QVBoxLayout()
        _mainLayout.setContentsMargins(25, 25, 25, 25)
        _mainLayout.setSpacing(15)
        self.setLayout(_mainLayout)

        _title = QLabel("Tasks", self)
        _title.setStyleSheet("""
        background-color: none;
        font-size: 25px;
        color: white;
        font-weight: bold;
        """)
        _title.adjustSize()

        _topPanel = QWidget(self)
        _buttonPanel = QHBoxLayout()
        _buttonPanel.setContentsMargins(0, 0, 0, 0)
        _topPanel.setLayout(_buttonPanel)
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
        _buttonPanel.addWidget(self._createButton)
        _buttonPanel.addWidget(self._filterButton)

        self._contentArea = QWidget(self)
        self._contentArea.setStyleSheet("background-color: transparent")
        self._layout3 = QVBoxLayout()
        self._layout3.setAlignment(Qt.AlignTop)
        self._layout3.setContentsMargins(0, 0, 0, 0)
        self._contentArea.setLayout(self._layout3)
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

        _mainLayout.addWidget(_title, stretch=0)
        _mainLayout.addWidget(_topPanel, stretch=0)
        _mainLayout.addWidget(_scroll, stretch=1)
        _mainLayout.activate()

        self._newTaskPopUp = newTask(self)
        self._newTaskPopUp.hide()
        self._newTaskPopUp.installEventFilter(self)
        self._createButton.clicked.connect(lambda: self._newTaskPopUp.createMode())

        self._filterTaskPopUp = filterTask(self)
        self._filterTaskPopUp.hide()
        self._filterTaskPopUp.installEventFilter(self)
        self._filterButton.clicked.connect(lambda: self._filterTaskPopUp.filterMode())

    def resizeEvent(self, event):
        """
        Function resizes the pop up based on the screen size. 
        This ensures visibility, readability and usability.
        """
        self._newTaskPopUp.setGeometry(self.rect())
        self._filterTaskPopUp.setGeometry(self.rect())

    def eventFilter(self, component, event): 
        """
        Function refreshes the data being displayed each time
        the pop up is closed. This ensures the data displayed is
        accurate and timely.
        """
        if event.type() == QEvent.Hide:
            self._displayTask(self._editor.filterTask(self._filterTaskPopUp.filterData()))
        return super().eventFilter(component, event)
           
    def _displayTask(self, data):
        """
        Function removes the old tasks being displayed to make
        way for the updated tasks to be displayed. Each data being 
        displayed includes an edit and delete button. 

        :param data: List of all the tasks that needs to be displayed.
        """
        while self._layout3.count():
            _data = self._layout3.takeAt(0)
            _widget = _data.widget()
            _widget.deleteLater()
         
        _allTask = data
        for _data in _allTask:
            _task = QWidget(self._contentArea)
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
            _check.clicked.connect(lambda checked, taskID = _data[0]: self._editor.markTask(taskID, QDate.currentDate().toString("d/M/yyyy")))
            _taskLayout.addWidget(_check, stretch=0)

            _detail = QWidget(_task)
            _detailLayout = QVBoxLayout()
            _detail.setLayout(_detailLayout)
            _taskName = QLabel(_data[2], _task)
            _taskName.setStyleSheet("font-weight: bold; font-size: 18px")
            _taskName.setWordWrap(True)
            _taskDetail = QLabel(f"{_data[8]}, Due Date: {_data[3]}")
            _taskDetail.setStyleSheet("font-size: 12px")
            _taskDetail.setWordWrap(True)
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
            _deleteButton.clicked.connect(lambda event, taskID = _data[0]: (self._editor.deleteTask(taskID), self._displayTask(self._editor.filterTask(self._filterTaskPopUp.filterData()))))
            _buttonLayout.addWidget(_editButton, stretch=0)
            _buttonLayout.addWidget(_deleteButton, stretch=0)
            _taskLayout.addWidget(_button, stretch=0)
            self._layout3.addWidget(_task, stretch=0)