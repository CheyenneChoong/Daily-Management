from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from schedule.schedule import *
from support.support import emotionalState

class newSchedule(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        background-color: rgba(77, 6, 83, 0.55);
        border-radius: 10px;
        """)

        _inputStyle = """
        border: 1px solid black;
        height: 40px;
        font-size: 16px;
        padding-left: 10px;
        padding-right: 10px;
        """
        _dateStyle = f"""
        QDateTimeEdit {{
            {_inputStyle}
        }}
        QDateTimeEdit::drop-down {{
            width: 30px;
            border: none;
        }}
        QDateTimeEdit::down-arrow {{
            image: url(icon/arrow.png);
            width: 12px;
            height: 12px;
        }}"""
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

        _mainLayout = QGridLayout()
        self.setLayout(_mainLayout)

        self._container = QWidget(self)
        self._container.setStyleSheet("background-color: white")
        _containerLayout = QVBoxLayout()
        self._container.setLayout(_containerLayout)

        self._title = QLabel("Add Event", self._container)
        self._title.setStyleSheet("""
        font-size: 25px;
        font-weight: bold;
        """)
        self._eventInput = QLineEdit(self._container)
        self._eventInput.setStyleSheet(_inputStyle)
        self._eventInput.setPlaceholderText("Event")
        self._eventInput.setToolTip("Event")
        self._eventInput.setMaxLength(40)
        self._venueInput = QLineEdit(self._container)
        self._venueInput.setStyleSheet(_inputStyle)
        self._venueInput.setPlaceholderText("Venue")
        self._venueInput.setToolTip("Venue")
        self._venueInput.setMaxLength(40)
        self._dateTimeInput = QDateTimeEdit()
        self._dateTimeInput.setStyleSheet(_dateStyle)
        self._dateTimeInput.setCalendarPopup(True)
        self._dateTimeInput.setDateTime(QDateTime.currentDateTime())
        self._dateTimeInput.setDisplayFormat("dd/MM/yyyy h:mm AP")
        _calendar = self._dateTimeInput.calendarWidget()
        _calendar.setStyleSheet(_calendarStyle)
        self._emotionInput = QListWidget(self._container)
        self._emotionInput.setStyleSheet("""
        border: 1px solid black;
        height: 60px;
        font-size: 16px;
        padding: 10px;
        """)
        self._emotionInput.setSelectionMode(QAbstractItemView.MultiSelection)

        _buttonPanel = QWidget(self._container)
        _buttonPanel.setStyleSheet("background-color: none;")
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
        self._actionButton = QPushButton("ADD", _buttonPanel)
        self._actionButton.clicked.connect(self._create)
        self._actionButton.setCursor(Qt.PointingHandCursor)
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

        _containerLayout.addWidget(self._title)
        _containerLayout.addWidget(self._eventInput)
        _containerLayout.addWidget(self._venueInput)
        _containerLayout.addWidget(self._dateTimeInput)
        _containerLayout.addWidget(self._emotionInput)
        _containerLayout.addWidget(_buttonPanel)
        _mainLayout.addWidget(self._container)

        self._scheduleEditor = schedule()
        self._emotionEditor = emotionalState()
        self._scheduleID = 0

    def _create(self):
        """
        Function for adding / updating an event. The data is processed
        and checked if null before added into the database to 
        avoid errors. Pop up hides if no error is found.
        """
        _event = self._eventInput.text().strip()
        _venue = self._venueInput.text().strip()
        _dateTime = self._dateTimeInput.text().strip()
        _emotions = self._emotionInput.selectedItems()
        if not _event or not _venue or not _dateTime or not _emotions:
            return
        
        _emotionIDs = []
        for _item in _emotions:
            _emotionIDs.append(_item.data(Qt.UserRole))

        if self._scheduleID > 0:
            self._scheduleEditor.edit(self._scheduleID, _event, _dateTime, _venue, _emotionIDs)
        else:
            self._scheduleEditor.create(_event, _dateTime, _venue, _emotionIDs)
        self.hide()
    
    def resizeEvent(self, event):
        """
        Functions resizes the container that contains the visible part
        of the pop up. This ensures the pop up is visible, usable and 
        accessible. This also ensures design consistency.
        """
        self._container.setFixedSize(int(self.width() * 0.63), int(self.height() * 0.5))
    
    def createMode(self):
        """
        Function that resets the pop up inputs for a create mode.
        This ensures no remainder data was left behind after edit mode
        if edit mode was in use.
        """
        self._title.setText("Add Event")
        self._eventInput.setText("")
        self._venueInput.setText("")
        self._emotionInput.clear()
        _emotionList = self._emotionEditor.emotion()
        for _emotion in _emotionList:
            _item = QListWidgetItem(_emotion[1])
            _item.setData(Qt.UserRole, _emotion[0])
            self._emotionInput.addItem(_item)
        self._actionButton.setText("ADD")
        self.show()
    
    def editMode(self, scheduleID):
        """
        Function that sets the pop up inputs for edit mode. 
        Displays the data of the event being edited. 

        :param scheduleID: The event being edited. 
        """
        self._scheduleID = scheduleID
        _eventData = self._scheduleEditor.singleSchedule(scheduleID)
        self._title.setText("Edit Event")
        self._eventInput.setText(_eventData[1])
        self._venueInput.setText(_eventData[3])
        self._dateTimeInput.setDateTime(QDateTime.fromString(_eventData[2], "dd/MM/yyyy h:mm AP"))
        _emotionList = self._emotionEditor.emotion()
        _scheduleEmotion = self._scheduleEditor.emotions(scheduleID)
        self._emotionInput.clear()
        for _emotion in _emotionList:
            _item = QListWidgetItem(_emotion[1])
            _item.setData(Qt.UserRole, _emotion[0])
            self._emotionInput.addItem(_item)
            if _emotion[0] in _scheduleEmotion:
                _item.setSelected(True)
        self._actionButton.setText("EDIT")
        self.show()