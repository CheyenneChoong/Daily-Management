# This file contains the class that focuses on the display of data and information.
# Data handling is done in a different file.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from task.taskPopup import *

class mainTask(QWidget) :
    def __init__(self): # Constructor function.
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True) # Ensures the Navigation is rendered.
        self.setStyleSheet("""
        background-color: rgba(209, 187, 255, 0.6);
        border-radius: 10px;
        """)

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
        self._searchInput = QLineEdit(_topPanel)
        self._searchInput.setStyleSheet("""
        height: 40px;
        font-size: 16px;
        padding-left: 10px;
        padding-right: 10px;
        """)
        self._searchInput.setPlaceholderText("Search...")
        self._searchButton = QPushButton("SEARCH", _topPanel)
        self._searchButton.setStyleSheet(_style)
        self._searchButton.setCursor(Qt.PointingHandCursor)
        _layout2.addWidget(self._createButton)
        _layout2.addWidget(self._filterButton)
        _layout2.addSpacing(int(self.width() * 0.4))
        _layout2.addWidget(self._searchInput)
        _layout2.addWidget(self._searchButton)

        # Filter Panel.
        # _filterPanel = QWidget(self)
        # _filterPanel.setStyleSheet("background-color: none;")
        # _layout3 = QHBoxLayout()
        # _layout3.setContentsMargins(0, 0, 0, 0)
        # _filterPanel.setLayout(_layout3)
        # self._filterButton = []
        # _buttonCount = 0
        # for _buttonName, _buttonFunction in zip(["Date", "Priority", "Category"], ["#", "#", "#"]):
        #     self._filterButton.append(QPushButton(_buttonName, _filterPanel))
        #     self._filterButton[_buttonCount].setCursor(Qt.PointingHandCursor)
        #     self._filterButton[_buttonCount].setStyleSheet("""
        #     QPushButton {
        #         background-color: #8660D3;
        #         height: 40px;
        #         font-weight: bold;
        #         font-size: 15px;
        #     }
        #     QPushButton:hover {
        #         background-color: #6B43B9;
        #     }
        #     """)
        #     _layout3.addWidget(self._filterButton[_buttonCount])
        #     _buttonCount += 1

        # Main content area where tasks are displayed.
        _contentArea = QWidget(self)
        self._layout4 = QHBoxLayout()

        # Adding all the widgets into the layout.
        _layout1.addWidget(_title, stretch=0)
        _layout1.addWidget(_topPanel, stretch=0)
        # _layout1.addWidget(_filterPanel, stretch=0)
        _layout1.addWidget(_contentArea, stretch=1)
        _layout1.activate()

        self._newTaskPopUp = newTask(self)
        self._newTaskPopUp.hide()
        self._createButton.clicked.connect(lambda: self._newTaskPopUp.show())

        self._filterTaskPopUp = filterTask(self)
        self._filterTaskPopUp.hide()
        self._filterButton.clicked.connect(lambda: self._filterTaskPopUp.show())

    def resizeEvent(self, event):
        self._newTaskPopUp.setGeometry(self.rect())
        self._filterTaskPopUp.setGeometry(self.rect())