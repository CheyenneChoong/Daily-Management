# This file contains the performance tab display. 
# The containers are imported from the feature that is related to it.

# Import module for UI.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Widgets.
from task.tasksSummary import taskSummary
from schedule.scheduleSummary import scheduleSummary

class mainPerformance(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        background-color: rgba(209, 187, 255, 0.6);
        border-radius: 10px;
        """)

        # Main layout.
        _mainLayout = QVBoxLayout()
        _mainLayout.setContentsMargins(25, 25, 25, 25)
        _mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(_mainLayout)

        # Title.
        _title = QLabel("Daily Overview", self)
        _title.setStyleSheet("""
        background-color: none;
        font-size: 25px;
        color: white;
        font-weight: bold;
        """)
        _title.adjustSize()

        # Widgets.
        _task = taskSummary()
        _schedule = scheduleSummary()

        # Add widgets to the main layout.
        _mainLayout.addWidget(_title, stretch = 0)
        _mainLayout.addWidget(_task, stretch = 1)
        _mainLayout.addWidget(_schedule, stretch = 1)