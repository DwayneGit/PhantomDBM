import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QPoint, Qt
from PyQt5.QtWidgets import QToolBar, QToolButton, QWidget, QAction, QLabel, QSizePolicy

from phantom.applicationSettings import settings

class PhtmTitleBar(QToolBar):
    def __init__(self, window, isMainWindow=False):
        super().__init__()
        
        self.window = window
        self.windowTitle = ""
        self.isMax = False
        self.isMainWindow = isMainWindow
        self.windowTitle = ""
        self.setObjectName("titleBar")

        self.setContextMenuPolicy(Qt.PreventContextMenu)

    def generateTitleBar(self):

        self.setMovable(False)
        self.setFixedHeight(36)
        self.setIconSize(QSize(19, 19))

        exitButton = QToolButton()
        exitButton.setDefaultAction(QAction(QIcon(settings.__ICONS__.close), "", self))

        if self.isMainWindow:
            # logo_bttn = QToolButton()
            # logo_bttn.setDefaultAction(QAction(QIcon(settings.__ICONS__.appIcon), "phantom", self))
            # logo_bttn.setObjectName("logo")
            # self.addWidget(logo_bttn)

            self.windowTitle = QLabel()
            self.addWidget(self.windowTitle)

            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.addWidget(spacer)

            minimizeButton = QToolButton()
            minimizeButton.setObjectName("title_button")
            minimizeButton.setDefaultAction(QAction(QIcon(settings.__ICONS__.minimze), "", self))
            minimizeButton.defaultAction().triggered.connect(self.window.showMinimized)
            self.addWidget(minimizeButton)

            maximizeButton = QToolButton()
            maximizeButton.setObjectName("title_button")
            maximizeButton.setDefaultAction(QAction(QIcon(settings.__ICONS__.maximize), "", self))
            maximizeButton.triggered.connect(lambda x: self.screenToggle(maximizeButton))
            self.addWidget(maximizeButton)

            exitButton.defaultAction().triggered.connect(sys.exit)
            exitButton.setObjectName("exit")

        else:
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.windowTitle = QLabel()
            self.addWidget(self.windowTitle)

            self.addWidget(spacer)

            exitButton.defaultAction().triggered.connect(self.dialogExit)
            exitButton.setObjectName("exit")

        self.addWidget(exitButton)

    def dialogExit(self):
        self.window.close()

    def screenToggle(self, toolButton):
        if not self.isMax:
            self.window.showMaximized()
            toolButton.setDefaultAction(QAction(QIcon(settings.__ICONS__.restore), "", self))
        elif self.isMax:
            self.window.showNormal()
            toolButton.setDefaultAction(QAction(QIcon(settings.__ICONS__.maximize), "", self))

        self.isMax = not self.isMax

    def mousePressEvent(self, event):
        self.window.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.window.oldPos)

        self.window.move(self.window.x() + delta.x(), self.window.y() + delta.y())
        self.window.oldPos = event.globalPos()

    def setWindowTitle(self, title):
        self.windowTitle.setText(title)