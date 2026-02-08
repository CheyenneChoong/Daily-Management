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
        self._layout = QGridLayout()
        self._layout.setContentsMargins(25, 15, 25, 15)
        self.setLayout(self._layout)

        self._content = QWidget(self)
        self._content.setStyleSheet("background-color: none;")
        self._contentLayout = QVBoxLayout()
        self._contentLayout.setContentsMargins(0, 0, 0, 0)
        self._contentLayout.setAlignment(Qt.AlignTop)
        self._content.setLayout(self._contentLayout)

        _scroll = QScrollArea()
        _scroll.setWidgetResizable(True)
        _scroll.setWidget(self._content)
        _scroll.setStyleSheet("""
        QScrollArea {
            background-color: transparent;
        } 
        QScrollBar:vertical { 
            background: black; 
            width: 4px; 
        }
        """)
        self._layout.addWidget(_scroll)

        try:
            _check = open("data/log.txt", "r")
            _check.close()
        except:
            _check = open("data/log.txt", "w")
            _check.close()

        with open("data/log.txt", "r") as _file:
            _check = _file.readline().strip()
            if not _check or QDate.fromString(_check, "M/d/yyyy") != QDate.currentDate():
                _rewrite = True
            else:
                _rewrite = False
        
        if _rewrite:
            with open("data/log.txt", "w") as _file:
                _file.write(f"{QDate.toString(QDate.currentDate(), "M/d/yyyy")}\n")
        
        self._display()

    def _display(self):
        while self._contentLayout.count():
            _message = self._contentLayout.takeAt(0)
            _message = _message.widget()
            _message.deleteLater()
        
        with open("data/log.txt", "r") as _file:
            for _line in _file:
                _message = QWidget(self._content)
                _message.setStyleSheet("background-color: none;")
                _messageLayout = QHBoxLayout()
                _messageLayout.setContentsMargins(0, 0, 0, 0)
                _message.setLayout(_messageLayout)
            
                _image = QLabel(_message)
                _image.setPixmap(QPixmap("icon/bts.png"))
                _messageLayout.addWidget(_image, stretch=0, alignment=Qt.AlignTop)

                _text = QLabel(_line, _message)
                _text.setStyleSheet("""
                font-size: 18px; 
                background-color: #ADE8FF;
                border-radius: 10px;
                padding: 10px;
                """)
                _text.setWordWrap(True)
                _messageLayout.addWidget(_text, stretch=1)

                self._contentLayout.addWidget(_message, stretch = 1)

        # self._hat = QWidget(self)
        # self._hat.setStyleSheet("""
        # background-color: #610C9B;
        # border-top-left-radius: 10px;
        # border-top-right-radius: 10px;
        # border-bottom-left-radius: 0;
        # border-bottom-right-radius: 0;
        # """)

        # self._content = QWidget(self)
    
    # def resizeEvent(self, event):
        # self._hat.resize(self.width(), int(self.height() * 0.13))
        # self._content.setMinimumWidth(self.width())

        # if (self.height() <= 80) :
        #     self._hat.hide()
        #     self._content.setMinimumHeight(self.height())
        #     self._content.move(0, 0)
        # else:
        #     self._hat.show()
        #     self._content.setMinimumHeight(int(self.height() * 0.83))
        #     self._content.move(self._content.x(), self._hat.height() + int(self.height() * 0.02))