# This file contains the class of the navigation panel.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Class for the Navigation panel.
class Navigation(QWidget) :
    def __init__(self, tab): # Constructor function.
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True) # Ensures the Navigation is rendered.
        self.setStyleSheet("""
        background-color: rgba(209, 187, 255, 0.6);
        border-radius: 10px;
        """)

        # Layout of the Navigation.
        self._layout = QHBoxLayout()
        self._layout.setSpacing(int(self.width() * 0.05))
        self.setLayout(self._layout)

        # Options within the navgation panel.
        self._option1 = QPushButton(self)
        self._option1.clicked.connect(lambda: tab.setCurrentIndex(0))
        self._option2 = QPushButton(self)
        self._option2.clicked.connect(lambda: tab.setCurrentIndex(1))
        self._option3 = QPushButton(self)
        self._option3.clicked.connect(lambda: tab.setCurrentIndex(2))
        self._option4 = QPushButton(self)
        self._option4.clicked.connect(lambda: tab.setCurrentIndex(3))

        # Adding the buttons to the layout.
        self._layout.addWidget(self._option1)
        self._layout.addWidget(self._option2)
        self._layout.addWidget(self._option3)
        self._layout.addWidget(self._option4)
    
    # Function for setting the button style.
    def _buttonStyle(self, _button, _iconName) :
        _style = """
        QPushButton {{
            background-color: #5000A1;
            border-radius: 15px;
            color: white;
            font-weight: bold;
            font-size: {}px;
        }}

        QPushButton:hover {{
            background-color: #321153;
        }}
        """.format(int(self._option1.height() * 0.3))
        _button.setIcon(QIcon(_iconName))
        _button.setStyleSheet(_style)
        _button.setCursor(Qt.PointingHandCursor)
    
    # Function to ensure the navigation layout and display is responsive to the resizing of the window.
    def resizeEvent(self, event):
        _buttonList = [self._option1, self._option2, self._option3, self._option4]
        _nameList = ["  Performance", "  Tasks To Do", "  Schedule", "  Monitoring"]
        _iconList = ["icon/performance.png", "icon/task.png", "icon/schedule.png", "icon/monitoring.png"]
        for _button, _name, _icon in zip(_buttonList, _nameList, _iconList):
            _button.setMinimumHeight(int(self.height() * 0.75))
            self._buttonStyle(_button, _icon)

            if self.width() >= 800 :
                _button.setText(_name)
                self._option1.setIconSize(QSize(int(self._option1.width() * 0.22) , int(self._option1.height() * 0.68)))
                self._option2.setIconSize(QSize(int(self._option2.width() * 0.16), int(self._option2.height() * 0.65)))
                self._option3.setIconSize(QSize(int(self._option3.width() * 0.22), int(self._option3.height() * 0.8)))
                self._option4.setIconSize(QSize(int(self._option4.width() * 0.22), int(self._option4.height() * 0.73)))
            else :
                _button.setText("")
                self._option1.setIconSize(QSize(int(self._option1.width() * 0.34), int(self._option1.height() * 0.80)))
                self._option2.setIconSize(QSize(int(self._option2.width() * 0.28), int(self._option2.height() * 0.77)))
                self._option3.setIconSize(QSize(int(self._option3.width() * 0.34), int(self._option3.height() * 0.92)))
                self._option4.setIconSize(QSize(int(self._option4.width() * 0.34), int(self._option4.height() * 0.85)))