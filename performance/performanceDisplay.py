from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from task.tasksSummary import taskSummary
from schedule.scheduleSummary import scheduleSummary

"""
mainPerformance class is for compiling the daily overview.
This is the first tab (Performance) and is the default tab
that would be displayed. It uses the taskSummary and 
schedule Summary class imported from the other features.
"""

class mainPerformance(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        background-color: rgba(209, 187, 255, 0.6);
        border-radius: 10px;
        """)

        _mainLayout = QVBoxLayout()
        _mainLayout.setContentsMargins(25, 25, 25, 25)
        _mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(_mainLayout)

        _title = QLabel("Daily Overview", self)
        _title.setStyleSheet("""
        background-color: none;
        font-size: 25px;
        color: white;
        font-weight: bold;
        """)
        _title.adjustSize()

        _task = taskSummary()
        _schedule = scheduleSummary()

        _mainLayout.addWidget(_title, stretch = 0)
        _mainLayout.addWidget(_task, stretch = 1)
        _mainLayout.addWidget(_schedule, stretch = 1)