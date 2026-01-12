# This file contains the class for the Notification Area.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Notification(QWidget) :
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True) # Ensures the Navigation is rendered.
        self.setStyleSheet("""
        background-color: rgba(209, 187, 255, 0.6);
        border-radius: 10px;
        """)

        self._hat = QWidget(self)
        self._hat.setStyleSheet("""
        background-color: #610C9B;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
        """)

        self._content = QWidget(self)
    
    def resizeEvent(self, event):
        self._hat.setMinimumWidth(self.width())
        self._hat.setMinimumHeight(int(self.height() * 0.13))
        self._content.setMinimumWidth(self.width())

        if (self.height() <= 75) :
            self._hat.hide()
            self._content.setMinimumHeight(self.height())
            self._content.move(0, 0)
        else:
            self._hat.show()
            self._content.setMinimumHeight(int(self.height() * 0.83))
            self._content.move(self._content.x(), self._hat.height() + int(self.height() * 0.02))