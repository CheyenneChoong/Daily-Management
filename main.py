"""
Daily Management Project
main.py serves as the starting point of the system (launch file).
"""

"""
Libraries / modules needed for designing and creating the GUI are imported.
The main display classes from each feature / component is imported to be connected through the main file.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from data.setupDB import *
from navigationArea.navigation import Navigation
from notificationArea.notification import Notification
from task.taskDisplay import mainTask
from support.supportDisplay import mainSupport
from schedule.scheduleDisplay import mainSchedule
from performance.performanceDisplay import mainPerformance

app = QApplication(sys.argv)

"""
Main class serves as the base / main window.
All the widgets are layered in this main window.
"""
class Main(QMainWindow) :
    def __init__(self):
        """
        Central widget is created to allow for the usage of GridLayout.
        3 main sections are created using the main display class of their sections and added into the layout
        The main area utilizes a tab widget to make the switch in tabs smooth.
        Each features' main display is added into the tab widget as its own tab option.
        """

        super().__init__()
        self.setWindowTitle('Daily Management')
        self.background = QPixmap('icon/background.png')
        self.setMinimumHeight(900)
        self.setWindowIcon(QIcon('icon/bts.png'))
        self.showMaximized()

        central = QWidget()
        self.setCentralWidget(central)
        
        self._layout = QGridLayout()
        self._layout.setSpacing(20)
        central.setLayout(self._layout)

        self._mainArea = QTabWidget()
        self._mainArea.tabBar().hide()
        self._mainArea.setStyleSheet("""
        QTabWidget::pane {
            background-color: transparent;
            border: 0;
        }
        """)
        self._mainArea.addTab(mainPerformance(), "Performance")
        self._mainArea.addTab(mainTask(), "Tasks")
        self._mainArea.addTab(mainSchedule(), "Schedule")
        self._mainArea.addTab(mainSupport(), "Support")

        self._navigationArea = Navigation(self._mainArea)
        self._notificationArea = Notification()
    
    def paintEvent(self, event):
        """
        Function is used to scale the background image to ensure 
        no matter what size window, the background image does not 
        look distorted and ensures consistency in the design.
        """
        painter = QPainter(self)
        scaled = self.background.scaled(self.size())
        painter.drawPixmap(0, 0, scaled)

    def resizeEvent(self, event):
        """
        Function is used to adjust the layout consistently based on
        the screen size. This ensures all components remain visible
        and design remains consistent regardless screen size.
        """
        if hasattr(self, "_layout"):
            _leftRight = int(self.width() * 0.04)
            _topBottom = int(self.height() * 0.04)
            self._layout.setContentsMargins(_leftRight, _topBottom, _leftRight, _topBottom)

        if self.width() >= 1000 and hasattr(self, "_layout") :
            self._layout.addWidget(self._navigationArea, 9, 5, 1, 11)
            self._layout.addWidget(self._notificationArea, 0, 0, 10, 4)
            self._layout.addWidget(self._mainArea, 0, 5, 9, 11)
            self._notificationArea.setMaximumWidth(484)
            self._notificationArea.setMaximumHeight(QWIDGETSIZE_MAX)
        
        if self.width() < 1000 and hasattr(self, "_layout") :
            self._notificationArea.setMaximumHeight(200)
            self._notificationArea.setMaximumWidth(QWIDGETSIZE_MAX)
            self._layout.addWidget(self._navigationArea, 9, 0, 1, 1)
            self._layout.addWidget(self._notificationArea, 0, 0, 1, 1)
            self._layout.addWidget(self._mainArea, 1, 0, 8, 1)

window = Main()
sys.exit(app.exec_())