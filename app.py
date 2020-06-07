import sys
import itertools
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QMainWindow, QMenu, QStyle, QSystemTrayIcon
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
import os

DURATION_INT = 1200
TIME_CYCLER = itertools.cycle([1200, 20])

def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        app.setStyle('Fusion')

        self.current_timer = 1
        self.time_left_int = DURATION_INT
        self.myTimer = QtCore.QTimer(self)

        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(QIcon(iconFile))
        self.tray_icon.show()

        #Tray menu
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(app.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # App window
        self.setGeometry(300, 300, 300, 180)
        self.setStyleSheet("background-color: #2B607A;")
        self.setWindowTitle("TwentyTwenty")

        # Widgets
        self.timerLabel = QtWidgets.QLabel(self)
        self.timerLabel.move(100,30)
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerLabel.setStyleSheet("font: 24pt ; color: white")

        self.startButton = QtWidgets.QPushButton(self)
        self.startButton.setText("Start")
        self.startButton.move(100,100)
        self.startButton.clicked.connect(self.startTimer)
        self.startButton.setStyleSheet("font: 20pt")
        self.startButton.setStyleSheet("font: 12pt ; background-color: #055076 ; color:white")

        self.minimizeButton = QtWidgets.QPushButton(self)
        self.minimizeButton.setText("Minimize")
        self.minimizeButton.move(100,130)
        self.minimizeButton.clicked.connect(self.minimize)
        self.minimizeButton.setStyleSheet("font: 12pt ; background-color: #055076 ; color:white")

        self.update_gui()

    def startTimer(self):
        self.time_left_int = next(TIME_CYCLER)
        self.myTimer.timeout.connect(self.timerTimeout)
        self.myTimer.start(1000)

    def timerTimeout(self):
        self.time_left_int -= 1
        if self.time_left_int == 0:
            if self.current_timer == 1:
                self.tray_icon.showMessage("TwentyTwenty", "It's time! Look away from your monitor for 20 seconds", QIcon(iconFile), 7000)
                self.current_timer = 2
            elif self.current_timer == 2:
                self.tray_icon.showMessage("TwentyTwenty", "Nice! You can now continue working", QIcon(iconFile), 7000)
                self.current_timer = 1
            self.time_left_int = next(TIME_CYCLER)

        self.update_gui()

    def update_gui(self):
        minsec = secs_to_minsec(self.time_left_int)
        self.timerLabel.setText(minsec)

    def minimize(self):
        self.hide()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Twenty Twenty",
            "Application was minimized to Tray",
            QIcon(iconFile),
            2000
        )

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
iconFile = resource_path('icon/icon.ico')
app = QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
main_window = App()
app.setWindowIcon(QIcon(iconFile))
main_window.show()
sys.exit(app.exec_())
