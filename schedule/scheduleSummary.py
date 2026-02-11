from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from schedule.schedule import schedule

class scheduleSummary(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        background-color: #E0ADFF;
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

        _title = QLabel("Today's Event", _topPanel)
        _title.setStyleSheet("""
        background-color: none;
        font-size: 20px;
        color: black;
        font-weight: bold;
        """)
        _title.adjustSize()
        _topPanelLayout.addWidget(_title, stretch = 1)

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
        _refreshButton.setCursor(Qt.PointingHandCursor)
        _refreshButton.clicked.connect(self._refreshData)
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
        Function refreshes the data being displayed. The already displayed events
        are removed to make way for the latest data to be displayed. This ensures
        the data displayed is accurate and timely. 
        """
        while self._containerLayout.count():
            _widget = self._containerLayout.takeAt(0)
            _widget = _widget.widget()
            _widget.deleteLater()

        _retriever = schedule()
        _todayEvents = _retriever.getSchedule(QDate.toString(QDate.currentDate(), "dd/MM/yyyy"))
        for _event in _todayEvents:
            _widget = QWidget(self._container)
            _widget.setStyleSheet("background-color: white")
            _widgetLayout = QVBoxLayout()
            _widgetLayout.setContentsMargins(25, 15, 25, 15)
            _widget.setLayout(_widgetLayout)

            _eventName = QLabel(_event[1], _widget)
            _eventName.setStyleSheet("font-weight: bold; font-size: 18px;")
            _eventDetail = QLabel(f"{_event[2]}, Venue: {_event[3]}")
            _eventDetail.setStyleSheet("font-size: 12px;")
            _widgetLayout.addWidget(_eventName)
            _widgetLayout.addWidget(_eventDetail)
            self._containerLayout.addWidget(_widget)