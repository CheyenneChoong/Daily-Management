# This file contains the code for the pop ups in the support system.
# The code for the data handling is in a separate file but is used here.

# Import libraries for GUI.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Import class for backend.
from support.support import emotionalState

# Styling.
_inputStyle = """
border: 1px solid black;
height: 40px;
font-size: 16px;
padding-left: 10px;
padding-right: 10px;
"""

# Class for add / edit emotional state.
class newEmotion(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        background-color: rgba(77, 6, 83, 0.55);
        border-radius: 10px;
        """)

        # Main layout.
        _mainLayout = QGridLayout()
        self.setLayout(_mainLayout)

        # The pop up area (visible in white.)
        self._container = QWidget(self)
        self._container.setStyleSheet("background-color: white")
        _containerLayout = QVBoxLayout()
        self._container.setLayout(_containerLayout)

        self._title = QLabel("Add Emotional State", self._container)
        self._title.setStyleSheet("""
        font-size: 25px;
        font-weight: bold;
        """)
        self._emotionInput = QLineEdit(self._container)
        self._emotionInput.setStyleSheet(_inputStyle)
        self._emotionInput.setPlaceholderText("Emotional State")
        self._emotionInput.setToolTip("Emotional State")
        self._emotionInput.setMaxLength(40)

        # Button panel.
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
        _containerLayout.addWidget(self._emotionInput)
        _containerLayout.addWidget(_buttonPanel)
        _mainLayout.addWidget(self._container)

        self._emotionalEditor = emotionalState()
        self._emotionID = 0
    
    def _create(self):
        _emotionalState = self._emotionInput.text().strip()
        if not _emotionalState:
            return
        
        if self._emotionID > 0:
            self._emotionalEditor.edit(self._emotionID, _emotionalState)
        else:
            self._emotionalEditor.create(_emotionalState)
        self.hide()
    
    def resizeEvent(self, event):
        self._container.setFixedSize(int(self.width() * 0.63), int(self.height() * 0.22))
    
    def createMode(self):
        self._emotionID = 0
        self._title.setText("Add Emotional State")
        self._emotionInput.setText("")
        self._actionButton.setText("ADD")
        self.show()
    
    def editMode(self, emotionID):
        self._emotionID = emotionID
        self._title.setText("Edit Emotional State")
        self._emotionInput.setText(self._emotionalEditor.singleEmotion(self._emotionID)[1])
        self._actionButton.setText("EDIT")
        self.show()

# Class for add / edit support.
class newSupport(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStylSheet("""
        background-color: rgba(77, 6, 83, 0.55);
        border-radius: 10px;
        """)

        # Main layout.
        _mainLayout = QGridLayout()
        self.setLayout(_mainLayout)