from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QInputDialog, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from phantom.utility import centerWindow

from . import PhtmTitleBar

class PhtmInputDialog(QDialog):
    def __init__(self, parent, title, msg, echoMode, text=None):
        super().__init__(parent) # set screen size (left, top, width, height

        # if not isinstance(centralDialog, QDialog):
        #     return "Pass central dialog is not of type QDialog"
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowModality(Qt.ApplicationModal)

        self.windowTitle = title

        self.parent = parent

        self.oldPos = self.pos()

        self.titleBar = PhtmTitleBar(self)
        self.titleBar.generateTitleBar()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)

        self.__layout.addWidget(self.titleBar)
        self.__inputDialog = QInputDialog()

        self.selectedValue = None
        if msg:
            self.__inputDialog.setLabelText(msg)
        self.__inputDialog.setTextEchoMode(echoMode)

        self.__inputDialog.textValueSelected.connect(self.valueSelected)
        self.__inputDialog.rejected.connect(self.reject)

        self.__layout.addWidget(self.__inputDialog)

        self.setLayout(self.__layout)

        # self.setGeometry(geometry)
        # self.move(centerWindow(self))

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(30, 30, 30))
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3)
        self.setGraphicsEffect(self.shadow)

        self.setWindowTitle(self.windowTitle)

    def valueSelected(self, value):
        self.selectedValue = value
        self.accept()

    def setWindowTitle(self, text):
        self.titleBar.setWindowTitle(text)
        self.setWindowTitle(text)
    
    def getWindowTitle(self):
        return self.titleBar.windowTitle

    def getLayout(self):
        return self.__layout

    def getInputDialog(self):
        return self.__inputBox