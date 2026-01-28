# This file contains the code that focuses on the display of data and UI.
# All data handling is done is a separate file.

# Import libraries for UI.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class mainSupport(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        background-color: rgba(209, 187, 255, 0.6);
        border-radius: 10px;
        """)

        