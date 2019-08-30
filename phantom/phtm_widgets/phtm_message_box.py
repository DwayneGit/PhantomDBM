from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from phantom.utility import centerWindow

from . import PhtmTitleBar

class PhtmMessageBox(QDialog):
    def __init__(self, parent, title, msg=None, buttons=None):
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
        self.__messageBox = QMessageBox()
        if msg:
            self.__messageBox.setText(msg)
        self.__buttonSet = {}
        if buttons:
            for btn in buttons:
                pushButton = self.__messageBox.addButton(btn)
                self.__buttonSet[str(pushButton)] = btn

        self.__layout.addWidget(self.__messageBox)

        self.setLayout(self.__layout)
        self.messageSelection = None

        self.__messageBox.buttonClicked.connect(self.closeBox)

        # self.setGeometry(geometry)
        # self.move(centerWindow(self))

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(30, 30, 30))
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3)
        self.setGraphicsEffect(self.shadow)

        self.setWindowTitle(self.windowTitle)

    def closeBox(self, button):
        if str(button) in self.__buttonSet:
            self.messageSelection = self.__buttonSet[str(button)]
        self.accept()

    def setWindowTitle(self, text):
        self.titleBar.setWindowTitle(text)
        self.setWindowTitle(text)
    
    def getWindowTitle(self):
        return self.titleBar.windowTitle

    def getLayout(self):
        return self.__layout

    def getMessageBox(self):
        return self.__messageBox