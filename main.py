# This file is the starting point and the code runs from here.
# The code here connects to other sections and provides the base display.

# Import PyQt5 libraries needed for the UI.
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

# Import code for setting up database.
from data.setupDB import *

# Import content.
from navigationArea.navigation import Navigation
from notificationArea.notification import Notification
from task.taskDisplay import mainTask
from support.supportDisplay import mainSupport
from schedule.scheduleDisplay import mainSchedule
from performance.performanceDisplay import mainPerformance

# Provides the environment to launch.
app = QApplication(sys.argv)

# Class that creates the main window launched.
class Main(QMainWindow) :
    def __init__(self): # Constructor function.
        super().__init__()

        # Sets up the window and background.
        self.setWindowTitle('Daily Management')
        self.background = QPixmap('icon/background.png')
        self.setMinimumHeight(900)
        self.setWindowIcon(QIcon('icon/bts.png'))
        self.showMaximized()

        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Sets layout for the areas.
        self._layout = QGridLayout()
        self._layout.setSpacing(20)
        central.setLayout(self._layout)

        # Main area.
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

        # Navigation and notification component.
        self._navigationArea = Navigation(self._mainArea)
        self._notificationArea = Notification()
    
    def paintEvent(self, event): # Function that adjusts the background based on the screen size.
        painter = QPainter(self)
        scaled = self.background.scaled(self.size())
        painter.drawPixmap(0, 0, scaled)

    def resizeEvent(self, event): # Function that adjusts the layout based on the window size.
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

# Launch the main class.
window = Main()

# Ensure the application exits when needed.
sys.exit(app.exec_())