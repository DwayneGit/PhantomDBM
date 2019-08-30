from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from phantom.utility import centerWindow

from . import PhtmTitleBar

class PhtmDialog(QDialog):
    def __init__(self, title, geometry, parent, centralDialog=None):
        super().__init__() # set screen size (left, top, width, height

        # if not isinstance(centralDialog, QDialog):
        #     return "Pass central dialog is not of type QDialog"
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowModality(Qt.ApplicationModal)

        self.__centralDialog = centralDialog

        self.windowTitle = title

        self.parent = parent

        self.oldPos = self.pos()

        self.titleBar = PhtmTitleBar(self)
        self.titleBar.generateTitleBar()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)

        self.__layout.addWidget(self.titleBar)
        if self.__centralDialog:
            self.__layout.addWidget(self.__centralDialog)

        self.setLayout(self.__layout)

        self.setGeometry(geometry)
        self.move(centerWindow(self))

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(30, 30, 30))
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3)
        self.setGraphicsEffect(self.shadow)

        self.setWindowTitle(self.windowTitle)

    def setWindowTitle(self, text):
        self.titleBar.setWindowTitle(text)
        self.setWindowTitle(text)

    def getWindowTitle(self):
        return self.titleBar.windowTitle

    def getLayout(self):
        return self.__layout

    def setCentralDialog(self, dialog):
        # if not isinstance(centralDialog, QDialog):
        #    throw  "Pass central dialog is not of type QDialog"
        if not self.__centralDialog:
            self.__layout.addWidget(dialog)
        self.__centralDialog = dialog

    def getCentralDialog(self):
        return self.__centralDialog