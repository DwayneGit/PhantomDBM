import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QPoint, Qt
from PyQt5.QtWidgets import QToolBar, QToolButton, QWidget, QAction, QLabel, QSizePolicy

from phantom.applicationSettings import settings

class PhtmTitleBar(QToolBar):
    def __init__(self, window, is_MainWindow=False):
        super().__init__()
        
        self.window = window
        self.windowTitle = ""
        self.is_max = False
        self.is_MainWindow = is_MainWindow
        self.windowTitle = ""
        self.setObjectName("titleBar")

        self.setContextMenuPolicy(Qt.PreventContextMenu)

    def generateTitleBar(self):

        self.setMovable(False)
        self.setFixedHeight(36)
        self.setIconSize(QSize(19, 19))

        exit_bttn = QToolButton()
        exit_bttn.setDefaultAction(QAction(QIcon(settings.__ICONS__.close), "", self))

        if self.is_MainWindow:
            # logo_bttn = QToolButton()
            # logo_bttn.setDefaultAction(QAction(QIcon(settings.__ICONS__.appIcon), "phantom", self))
            # logo_bttn.setObjectName("logo")
            # self.addWidget(logo_bttn)

            self.windowTitle = QLabel()
            self.addWidget(self.windowTitle)

            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.addWidget(spacer)

            min_bttn = QToolButton()
            min_bttn.setObjectName("title_button")
            min_bttn.setDefaultAction(QAction(QIcon(settings.__ICONS__.minimze), "", self))
            min_bttn.defaultAction().triggered.connect(self.window.showMinimized)
            self.addWidget(min_bttn)

            screen_bttn = QToolButton()
            screen_bttn.setObjectName("title_button")
            screen_bttn.setDefaultAction(QAction(QIcon(settings.__ICONS__.maximize), "", self))
            screen_bttn.triggered.connect(lambda x: self.screen_toggle(screen_bttn))
            self.addWidget(screen_bttn)

            exit_bttn.defaultAction().triggered.connect(sys.exit)
            exit_bttn.setObjectName("exit")

        else:
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.windowTitle = QLabel()
            self.addWidget(self.windowTitle)

            self.addWidget(spacer)

            exit_bttn.defaultAction().triggered.connect(self.dialog_exit)
            exit_bttn.setObjectName("exit")

        self.addWidget(exit_bttn)

    def dialog_exit(self):
        self.window.close()

    def screen_toggle(self, tool_button):
        if not self.is_max:
            self.window.showMaximized()
            tool_button.setDefaultAction(QAction(QIcon(settings.__ICONS__.restore), "", self))
        elif self.is_max:
            self.window.showNormal()
            tool_button.setDefaultAction(QAction(QIcon(settings.__ICONS__.maximize), "", self))

        self.is_max = not self.is_max

    def mousePressEvent(self, event):
        self.window.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.window.oldPos)

        self.window.move(self.window.x() + delta.x(), self.window.y() + delta.y())
        self.window.oldPos = event.globalPos()

    def setWindowTitle(self, title):
        self.windowTitle.setText(title)