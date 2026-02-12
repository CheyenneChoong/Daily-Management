from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from support.support import emotionalState, support

"""
newEmotion and newSupport are pop ups for create / update data.
Both classes share the same structure (except different data to process).

:func _create: Create a new data provided the mode is not edit mode otherwise edits the data.
:func resizeEvent: Resizes the visible container that contains the data. Ensures the display
is visible and readable.
:func createMode: Resets the data for create mode.
:func editMode: Displays the data of the data being edited. 
"""

_inputStyle = """
border: 1px solid black;
height: 40px;
font-size: 16px;
padding-left: 10px;
padding-right: 10px;
"""

class newEmotion(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
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

        self._title = QLabel("Add Emotional State", self._container)
        self._title.setStyleSheet("""
        font-size: 25px;
        font-weight: bold;
        """)
        self._emotionInput = QLineEdit(self._container)
        self._emotionInput.setStyleSheet(_inputStyle)
        self._emotionInput.setPlaceholderText("Emotional State")
        self._emotionInput.setToolTip("Emotional State")

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

class newSupport(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
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

        self._title = QLabel("Add Support", self._container)
        self._title.setStyleSheet("""
        font-size: 25px;
        font-weight: bold;
        """)
        self._supportInput = QLineEdit(self._container)
        self._supportInput.setStyleSheet(_inputStyle)
        self._supportInput.setPlaceholderText("Support")
        self._supportInput.setToolTip("Support")
        self._linkInput = QLineEdit(self._container)
        self._linkInput.setStyleSheet(_inputStyle)
        self._linkInput.setPlaceholderText("Link")
        self._linkInput.setToolTip("Link")
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
        _containerLayout.addWidget(self._supportInput)
        _containerLayout.addWidget(self._linkInput)
        _containerLayout.addWidget(self._emotionInput)
        _containerLayout.addWidget(_buttonPanel)
        _mainLayout.addWidget(self._container)

        self._supportID = 0
        self._supportEditor = support()
        self._emotionalEditor = emotionalState()
    
    def _create(self):
        _support = self._supportInput.text().strip()
        _link = self._linkInput.text().strip()
        _emotions = self._emotionInput.selectedItems()
        if not _support or not _link or not _emotions:
            return
        
        _emotionIDs = []
        for _item in _emotions:
            _emotionIDs.append(_item.data(Qt.UserRole))
        
        if self._supportID > 0:
            self._supportEditor.edit(self._supportID, _support, _link, _emotionIDs)
        else:
            self._supportEditor.create(_support, _link, _emotionIDs)
        self.hide()
    
    def resizeEvent(self, event):
        self._container.setFixedSize(int(self.width() * 0.63), int(self.height() * 0.5))
    
    def createMode(self):
        self._supportID = 0
        self._title.setText("Add Support")
        self._supportInput.setText("")
        self._linkInput.setText("")
        _emotionList = self._emotionalEditor.emotion()
        self._emotionInput.clear()
        for _emotion in _emotionList:
            _item = QListWidgetItem(_emotion[1])
            _item.setData(Qt.UserRole, _emotion[0])
            self._emotionInput.addItem(_item)
        self._actionButton.setText("ADD")
        self.show()
    
    def editMode(self, supportID):
        self._supportID = supportID
        self._title.setText("Edit Support")
        _supportData = self._supportEditor.singleSupport(supportID)
        self._supportInput.setText(_supportData[1])
        self._linkInput.setText(_supportData[2])
        _emotionList = self._emotionalEditor.emotion()
        _supportEmotion = self._supportEditor.emotions(supportID)
        self._emotionInput.clear()
        for _emotion in _emotionList:
            _item = QListWidgetItem(_emotion[1])
            _item.setData(Qt.UserRole, _emotion[0])
            self._emotionInput.addItem(_item)
            if _emotion[0] in _supportEmotion:
                _item.setSelected(True)
        self._actionButton.setText("EDIT")
        self.show()