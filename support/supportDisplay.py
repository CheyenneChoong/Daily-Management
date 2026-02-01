# This file contains the code that focuses on the display of data and UI.
# All data handling is done is a separate file.

# Import libraries for UI.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Import pop up.
from support.supportPopup import *
from support.support import *

class mainSupport(QWidget):
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

        # Title Panel.
        _mainTitle = QLabel("Emotion Regulator", self)
        _mainTitle.setStyleSheet(_titleStyle + "font-size: 25px;")
        _mainTitle.adjustSize()

        # Section 1 - Emotional State Section.
        _section1 = QWidget(self)
        _section1.setStyleSheet("background-color: none;")
        _layout1 = QHBoxLayout()
        _layout1.setContentsMargins(0, 0, 0, 0)
        _section1.setLayout(_layout1)
        
        _title1 = QLabel("Emotional State", self)
        _title1.setStyleSheet(_titleStyle + "font-size: 20px;")
        _title1.adjustSize()
        _addButton1 = QPushButton("ADD", _section1)
        _addButton1.setStyleSheet(_buttonStyle)
        _addButton1.setFixedWidth(200)
        _addButton1.setCursor(Qt.PointingHandCursor)
        _layout1.addWidget(_title1, stretch=0)
        _layout1.addWidget(_addButton1, stretch=0)

        self._content1 = QWidget(self)
        self._content1.setStyleSheet("background-color: none;")
        self._contentLayout1 = QVBoxLayout()
        self._contentLayout1.setAlignment(Qt.AlignTop)
        self._contentLayout1.setContentsMargins(0, 0, 0, 0)
        self._content1.setLayout(self._contentLayout1)
        _scroll1 = QScrollArea()
        _scroll1.setWidgetResizable(True)
        _scroll1.setWidget(self._content1)
        _scroll1.setStyleSheet(_scrollStyle)

        # Section 2 - Emotional Support
        _section2 = QWidget(self)
        _section2.setStyleSheet("background-color: none;")
        _layout2 = QHBoxLayout()
        _layout2.setContentsMargins(0, 0, 0, 0)
        _section2.setLayout(_layout2)

        _title2 = QLabel("Emotional Support", self)
        _title2.setStyleSheet(_titleStyle + "font-size: 20px;")
        _title2.adjustSize()
        _addButton2 = QPushButton("ADD", _section2)
        _addButton2.setStyleSheet(_buttonStyle)
        _addButton2.setFixedWidth(200)
        _addButton2.setCursor(Qt.PointingHandCursor)
        _layout2.addWidget(_title2, stretch=0)
        _layout2.addWidget(_addButton2, stretch=0)

        self._content2 = QWidget(self)
        self._content2.setStyleSheet("background-color: none;")
        self._contentLayout2 = QVBoxLayout()
        self._contentLayout2.setAlignment(Qt.AlignTop)
        self._contentLayout2.setContentsMargins(0, 0, 0, 0)
        self._content2.setLayout(self._contentLayout2)
        _scroll2 = QScrollArea()
        _scroll2.setWidgetResizable(True)
        _scroll2.setWidget(self._content2)
        _scroll2.setStyleSheet(_scrollStyle)

        # Add all the widgets to the main layout.
        _mainLayout.addWidget(_mainTitle)
        _mainLayout.addWidget(_section1)
        _mainLayout.addWidget(_scroll1)
        _mainLayout.addWidget(_section2)
        _mainLayout.addWidget(_scroll2)

        self._newEmotionPopup = newEmotion(self)
        self._newEmotionPopup.hide()
        self._newEmotionPopup.installEventFilter(self)
        _addButton1.clicked.connect(lambda: self._newEmotionPopup.createMode())

        self._emotionEditor = emotionalState()
        self._displayEmotion()
    
    def resizeEvent(self, event):
        self._newEmotionPopup.setGeometry(self.rect())
    
    def eventFilter(self, component, event):
        if event.type() == QEvent.Hide:
            self._displayEmotion()
        return super().eventFilter(component, event)

    def _displayEmotion(self):
        while self._contentLayout1.count():
            _data = self._contentLayout1.takeAt(0)
            _widget = _data.widget()
            _widget.deleteLater()

        _allEmotion = self._emotionEditor.emotion()
        for _data in _allEmotion:
            _emotion = QWidget(self._content1)
            _emotion.setMaximumHeight(65)
            _emotion.setStyleSheet("background-color: white")
            _emotionLayout = QHBoxLayout()
            _emotionLayout.setContentsMargins(25, 0, 25, 0)
            _emotion.setLayout(_emotionLayout)

            _emotionalState = QLabel(_data[1], _emotion)
            _emotionalState.setStyleSheet("font-weight: bold; font-size: 18px;")
            _emotionLayout.addWidget(_emotionalState, stretch = 1)

            _button = QWidget(_emotion)
            _buttonLayout = QHBoxLayout()
            _button.setLayout(_buttonLayout)
            _editButton = QPushButton(_button)
            _editButton.setIcon(QIcon("icon/edit.png"))
            _editButton.setIconSize(QSize(25, 25))
            _editButton.clicked.connect(lambda event, emotionID = _data[0]: self._newEmotionPopup.editMode(emotionID))
            _deleteButton = QPushButton(_button)
            _deleteButton.setIcon(QIcon("icon/delete.png"))
            _deleteButton.setIconSize(QSize(25, 25))
            _deleteButton.clicked.connect(lambda event, emotionID = _data[0]: (self._emotionEditor.delete(emotionID), self._displayEmotion()))
            _buttonLayout.addWidget(_editButton, stretch=0)
            _buttonLayout.addWidget(_deleteButton, stretch=0)
            _emotionLayout.addWidget(_button)

            self._contentLayout1.addWidget(_emotion)
    
    def _displaySupport(self):
        print("Support")
