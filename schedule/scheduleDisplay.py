# This file contains the code focused on displaying the schedule feature.
# Data handling is done in a separate file.

# Import modules for UI.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Import pop up and editor.
from schedule.schedulePopup import newSchedule
from schedule.schedule import schedule

class mainSchedule(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        background-color: rgba(209, 187, 255, 0.6);
        border-radius: 10px;
        """)

        # Set up the main layout.
        _mainLayout = QVBoxLayout()
        _mainLayout.setContentsMargins(25, 25, 25, 25)
        _mainLayout.setSpacing(15)
        _mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(_mainLayout)

        # Variables containing the styling for certain components.
        _titleStyle = """
        background-color: none;
        color: white;
        font-weight: bold;
        """
        _buttonStyle = """
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
        _scrollStyle = """
        QScrollArea {
            background-color: transparent;
        } 
        QScrollBar:vertical { 
            background: black; 
            width: 4px; 
        }
        """
        _inputStyle = """
        border: 1px solid black;
        height: 40px;
        font-size: 16px;
        padding-left: 10px;
        padding-right: 10px;
        """

        # Title Panel.
        _title = QLabel("Schedule", self)
        _title.setStyleSheet(_titleStyle + "font-size: 25px;")
        _title.adjustSize()
        
        # Calendar widget.
        self._calendar = QCalendarWidget(self)
        self._calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self._calendar.setStyleSheet("""
        QCalendarWidget QTableView { 
            background-color: white; 
        }
        QCalendarWidget QTableView::item:selected { 
            background-color: purple;
        }
        """)
        self._calendar.clicked.connect(lambda: self._displaySchedule(self._scheduleEditor.getSchedule(self._calendar.selectedDate().toString("MM/dd/yyyy"))))

        # Add and filter panel.
        _panel = QWidget(self)
        _panelLayout = QHBoxLayout()
        _panelLayout.setContentsMargins(0, 0, 0, 0)
        _panel.setLayout(_panelLayout)
        _panel.setStyleSheet("background-color: none;")
        _addButton = QPushButton("ADD", _panel)
        _addButton.setStyleSheet(_buttonStyle)
        _addButton.setCursor(Qt.PointingHandCursor)
        self._searchInput = QLineEdit(_panel)
        self._searchInput.setStyleSheet(_inputStyle)
        self._searchInput.setPlaceholderText("Search...")
        _searchButton = QPushButton("SEARCH", _panel)
        _searchButton.setStyleSheet(_buttonStyle)
        _searchButton.setCursor(Qt.PointingHandCursor)
        _searchButton.clicked.connect(lambda: self._displaySchedule(self._scheduleEditor.getSchedule(self._searchInput.text().strip())))
        _panelLayout.addWidget(_addButton)
        _panelLayout.addSpacing(int(self.width() * 0.5))
        _panelLayout.addWidget(self._searchInput)
        _panelLayout.addWidget(_searchButton)

        # Container for displaying the events.
        self._container = QWidget(self)
        self._container.setStyleSheet("background-color: none;")
        self._containerLayout = QVBoxLayout()
        self._containerLayout.setAlignment(Qt.AlignTop)
        self._containerLayout.setContentsMargins(0, 0, 0, 0)
        self._container.setLayout(self._containerLayout)
        _scroll = QScrollArea()
        _scroll.setWidgetResizable(True)
        _scroll.setWidget(self._container)
        _scroll.setStyleSheet(_scrollStyle)

        # Add widgets to mainlayout.
        _mainLayout.addWidget(_title, stretch=0)
        _mainLayout.addWidget(self._calendar, stretch=1)
        _mainLayout.addWidget(_panel, stretch=0)
        _mainLayout.addWidget(_scroll, stretch=1)

        # Pop up.
        self._newSchedulePopup = newSchedule(self)
        self._newSchedulePopup.hide()
        self._newSchedulePopup.installEventFilter(self)
        _addButton.clicked.connect(lambda: self._newSchedulePopup.createMode())

        self._scheduleEditor = schedule()
        self._displaySchedule(self._scheduleEditor.getSchedule(False))
    
    def resizeEvent(self, event):
        self._newSchedulePopup.setGeometry(self.rect())
    
    def eventFilter(self, component, event):
        if event.type() == QEvent.Hide:
            _search = self._searchInput.text().strip()
            self._displaySchedule(self._scheduleEditor.getSchedule(_search))
        return super().eventFilter(component, event)
    
    def _displaySchedule(self, scheduleData):
        _allSchedule = scheduleData
        while self._containerLayout.count():
            _data = self._containerLayout.takeAt(0)
            _widget = _data.widget()
            _widget.deleteLater()

        for _data in _allSchedule:
            _highlightDateTime = QDateTime.fromString(_data[2], "MM/dd/yyyy h:mm AP")
            _highlightDate = _highlightDateTime.date()
            _format = QTextCharFormat()
            _format.setBackground(QBrush(QColor("#B49DE5")))
            _format.setFontWeight(75)
            self._calendar.setDateTextFormat(_highlightDate, _format)

            _schedule = QWidget(self._container)
            _schedule.setMaximumHeight(65)
            _schedule.setStyleSheet("background-color: white")
            _scheduleLayout = QHBoxLayout()
            _scheduleLayout.setContentsMargins(25, 0, 25, 0)
            _schedule.setLayout(_scheduleLayout)

            _detail = QWidget(_schedule)
            _detailLayout = QVBoxLayout()
            _detail.setLayout(_detailLayout)
            _eventName = QLabel(_data[1], _detail)
            _eventName.setStyleSheet("font-weight: bold; font-size: 18px;")
            _eventDetail = QLabel(f"{_data[2]}, Venue: {_data[3]}")
            _eventDetail.setStyleSheet("font-size: 12px;")
            _detailLayout.addWidget(_eventName)
            _detailLayout.addWidget(_eventDetail)
            
            _button = QWidget(_schedule)
            _buttonLayout = QHBoxLayout()
            _button.setLayout(_buttonLayout)
            _editButton = QPushButton(_button)
            _editButton.setIcon(QIcon("icon/edit.png"))
            _editButton.setIconSize(QSize(25, 25))
            _editButton.clicked.connect(lambda event, scheduleID = _data[0]: self._newSchedulePopup.editMode(scheduleID))
            _deleteButton = QPushButton(_button)
            _deleteButton.setIcon(QIcon("icon/delete.png"))
            _deleteButton.setIconSize(QSize(25, 25))
            _deleteButton.clicked.connect(lambda event, scheduleID = _data[0]: {self._scheduleEditor.delete(scheduleID), self._displaySchedule(self._scheduleEditor.getSchedule(self._searchInput.text().strip()))})
            _buttonLayout.addWidget(_editButton)
            _buttonLayout.addWidget(_deleteButton)

            _scheduleLayout.addWidget(_detail, stretch = 1)
            _scheduleLayout.addWidget(_button, stretch = 0)
            self._containerLayout.addWidget(_schedule, stretch=0)