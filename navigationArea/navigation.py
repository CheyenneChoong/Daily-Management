"""
navigation.py focuses on the navigation bar.
This is what the user uses to switch between tabs
in the main display section.
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Navigation(QWidget) :
    def __init__(self, tab):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        background-color: rgba(209, 187, 255, 0.6);
        border-radius: 10px;
        """)

        self._layout = QHBoxLayout()
        self._layout.setSpacing(int(self.width() * 0.05))
        self.setLayout(self._layout)

        # The 4 tab options with its connection to the main QTabWidget.
        self._option1 = QPushButton(self)
        self._option1.clicked.connect(lambda: tab.setCurrentIndex(0))
        self._option2 = QPushButton(self)
        self._option2.clicked.connect(lambda: tab.setCurrentIndex(1))
        self._option3 = QPushButton(self)
        self._option3.clicked.connect(lambda: tab.setCurrentIndex(2))
        self._option4 = QPushButton(self)
        self._option4.clicked.connect(lambda: tab.setCurrentIndex(3))

        self._layout.addWidget(self._option1)
        self._layout.addWidget(self._option2)
        self._layout.addWidget(self._option3)
        self._layout.addWidget(self._option4)
    
    def _buttonStyle(self, _button, _icon) :
        """
        Function is used to simplify the button styling process.
        As all buttons used the same style, the function can be looped through for styling purposes.

        :param _button: QPushButton widget that is going to be styled.
        :param _icon: Icon used for the button.
        """

        _button.setIcon(QIcon(_icon))
        _button.setStyleSheet(f"""
        QPushButton {{
            background-color: #5000A1;
            border-radius: 15px;
            color: white;
            font-weight: bold;
            font-size: {int(self._option1.height() * 0.3)}px;
        }}

        QPushButton:hover {{
            background-color: #321153;
        }}
        """)
        _button.setCursor(Qt.PointingHandCursor)
  
    def resizeEvent(self, event):
        """
        Function is used to adjust the layout and display of the navigation bar.
        This ensures the navigation bar remains visible, understandable and usable.
        This also ensures the responsiveness of the design regardless of screen size.
        """

        _buttonList = [self._option1, self._option2, self._option3, self._option4]
        _nameList = ["  Performance", "  Tasks To Do", "  Schedule", "  Support"]
        _iconList = ["icon/performance.png", "icon/task.png", "icon/schedule.png", "icon/support.png"]
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