from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from windows_toasts import *
import sqlite3
import random
import threading

def Notify(message):
    try:
        _toaster = WindowsToaster("Daily Management")
        _toast = Toast()
        _toast.text_fields = ["BTS", message]
        _toast.images.append(ToastDisplayImage(ToastImage("icon/bts.png"), "BTS", ToastImagePosition.AppLogo, True))
        _toaster.show_toast(_toast)
    except Exception as e:
        print(f"Exception: {e}")

class Notification(QWidget) :
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
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
            _check = _file.readline().strip().split("|")[0]
            if not _check or QDate.fromString(_check, "M/d/yyyy") != QDate.currentDate():
                _rewrite = True
            else:
                _rewrite = False
        
        if _rewrite:
            with open("data/log.txt", "w") as _file:
                _file.write(f"{QDate.toString(QDate.currentDate(), "M/d/yyyy")}|Today is {QDate.toString(QDate.currentDate(), "dddd, d MMMM yyyy")}.\n")
        
        self._overview()
        self._refresh()
        self._timer = QTimer()
        self._timer.timeout.connect(self._refresh)
        self._timer.start(10000)

    def _display(self):
        while self._contentLayout.count():
            _message = self._contentLayout.takeAt(0)
            _message = _message.widget()
            _message.deleteLater()
        
        with open("data/log.txt", "r") as _file:
            for _line in _file:
                _line = _line.split("|")
                _message = QWidget(self._content)
                _message.setStyleSheet("background-color: none;")
                _messageLayout = QHBoxLayout()
                _messageLayout.setContentsMargins(0, 0, 0, 0)
                _message.setLayout(_messageLayout)
            
                _image = QLabel(_message)
                _image.setPixmap(QPixmap("icon/bts.png"))
                _messageLayout.addWidget(_image, stretch=0, alignment=Qt.AlignTop)

                _text = QLabel(_line[1], _message)
                _text.setStyleSheet("""
                font-size: 18px; 
                background-color: #ADE8FF;
                border-radius: 10px;
                padding: 10px;
                """)
                _text.setWordWrap(True)
                _messageLayout.addWidget(_text, stretch = 1, alignment=Qt.AlignTop)
                self._contentLayout.addWidget(_message, stretch = 1, alignment=Qt.AlignTop)
        
        _endWidget = QWidget(self._content)
        _endWidget.setStyleSheet("background-color: none;")
        self._contentLayout.addWidget(_endWidget, stretch = 10)
    
    def _overview(self):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _tasks = _cursor.execute(f"SELECT COUNT(executeDate) FROM tasks WHERE executeDate = '{QDate.toString(QDate.currentDate(), "M/d/yyyy")}';")
        _tasks = _tasks.fetchone()
        _events = _cursor.execute(f"SELECT COUNT(event) FROM schedule WHERE dateTime LIKE '%{QDate.toString(QDate.currentDate(), "M/d/yyyy")}%';")
        _events = _events.fetchone()
        with open("data/log.txt", "a") as _file:
            _file.write(f"overview|{QDateTime.toString(QDateTime.currentDateTime(), "h:mm AP")} Totals tasks to complete today is {_tasks[0]}. Events scheduled for today is {_events[0]}.\n")
        _connect.commit()
        _connect.close()
    
    def _refresh(self):
        self._progress()
        self._events()
        self._display()

    def _progress(self):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()

        _completed = _cursor.execute(f"SELECT COUNT(completionDate) FROM tasks WHERE completionDate = '{QDate.toString(QDate.currentDate(), "M/d/yyyy")}';")
        _completed = _completed.fetchone()
        _total = _cursor.execute(f"SELECT COUNT(executeDate) FROM tasks WHERE executeDate = '{QDate.toString(QDate.currentDate(), "M/d/yyyy")}';")
        _total = _total.fetchone()
        if _total[0] > 0:
            _taskProgress = int(_completed[0] / _total[0] * 100)
        else:
            _taskProgress = 0

        if _taskProgress == 25:
            _key = "T25%"
        elif _taskProgress > 25 and _taskProgress <= 50:
            _key = "T50%"
        elif _taskProgress > 50 and _taskProgress <= 75:
            _key = "T75%"
        elif _taskProgress == 100:
            _key = "T100%"
        else:
            _key = None
        
        with open("data/log.txt", "r") as _file:
            for _line in _file:
                _line = _line.split("|")[0]
                if _line == _key or not _key:
                    _write = False
                    break
                _write = True
            
        if _write:
            with open("data/log.txt", "a") as _file:
                _file.write(f"{_key}|You have completed {_taskProgress}% of the tasks needed to be completed today.\n")
                _allSupport = _cursor.execute("SELECT name, link FROM support;")
                _allSupport = _allSupport.fetchall()
                if len(_allSupport) > 0:
                    _random = random.randint(1, len(_allSupport))
                    _support = _allSupport[_random-1]
                    _file.write(f"support|Here's a recommended support for you. <a href='{_support[1]}' style='color: purple; text-decoration: none'>{_support[0]}</a>.\n")

        _connect.commit()
        _connect.close()
    
    def _events(self):
        _connect = sqlite3.connect("data/database.db")
        _cursor = _connect.cursor()
        _allEvent = _cursor.execute(f"SELECT * FROM schedule WHERE dateTime LIKE '%{QDate.toString(QDate.currentDate(), "M/d/yyyy")}%';")
        _allEvent = _allEvent.fetchall()
        _messages = []
        _notify = []
        for _event in _allEvent:
            _time = QDateTime.fromString(_event[2], "M/d/yyyy h:mm AP")
            _current = QDateTime.currentDateTime()
            _difference = _current.secsTo(_time) // 60
            if _difference <= 60 and _difference >= 0:
                _messages.append([f"S{_event[0]}Before", f"You have {_event[1]} at {_event[2]} scheduled in {_difference} minutes."])
                _notify.append(f"You have {_event[1]} at {_event[2]} scheduled in {_difference} minutes.")
            elif _difference < -60:
                _emotions = _cursor.execute(f"SELECT emotionID FROM scheduleState WHERE scheduleID = {_event[0]};")
                _emotions = _emotions.fetchall()
                _supportList = []
                for _emotion in _emotions:
                    _allSupport = _cursor.execute(f"""SELECT s.name, s.link FROM emotionalSupport e 
                                                  LEFT JOIN support s ON e.supportID = s.supportID
                                                  WHERE e.emotionID = {_emotion[0]};""")
                    _allSupport = _allSupport.fetchall()
                    if len(_allSupport) > 0:
                        _random = random.randint(1, len(_allSupport))
                        _support = _allSupport[_random-1]
                        _supportList.append(f"<a href='{_support[1]}' style='color: purple; text-decoration: none'>{_support[0]}</a>.")
                    _messages.append([f"S{_event[0]}After", f"How was {_event[1]}? Here is some emotional support for you. {",".join(_supportList)}."])
                    _notify.append(f"How was {_event[1]}?")

        with open("data/log.txt", "r") as _file:
            for _line in _file:
                _line = _line.split("|")[0]
                for _message, _currentNotify in zip(_messages, _notify):
                    if _line == _message[0]:
                        _messages.remove(_message)
                        _notify.remove(_currentNotify)
        
        with open("data/log.txt", "a") as _file:
            for _message, _currentNotify in zip(_messages, _notify):
                _file.write(f"{_message[0]}|{_message[1]}\n")
                _thread = threading.Thread(target=Notify, args=(_currentNotify,))
                _thread.start()
        
        _connect.commit()
        _connect.close()