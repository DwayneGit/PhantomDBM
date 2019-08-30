from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from phantom.utility import centerWindow

from . import PhtmTitleBar

class PhtmMessageBox(QDialog):
    def __init__(self, parent, title, msg=None, buttons=None):
        super().__init__(parent) # set screen size (left, top, width, height

        # if not isinstance(central_dialog, QDialog):
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
        self.__message_box = QMessageBox()
        if msg:
            self.__message_box.setText(msg)
        self.__button_set = {}
        if buttons:
            for btn in buttons:
                push_btn = self.__message_box.addButton(btn)
                self.__button_set[str(push_btn)] = btn

        self.__layout.addWidget(self.__message_box)

        self.setLayout(self.__layout)
        self.msg_selection = None

        self.__message_box.buttonClicked.connect(self.close_box)

        # self.setGeometry(geometry)
        # self.move(centerWindow(self))

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(30, 30, 30))
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3)
        self.setGraphicsEffect(self.shadow)

        self.setWindowTitle(self.windowTitle)

    def close_box(self, button):
        if str(button) in self.__button_set:
            self.msg_selection = self.__button_set[str(button)]
        self.accept()

    def setWindowTitle(self, text):
        self.titleBar.setWindowTitle(text)
        self.setWindowTitle(text)
    
    def getWindowTitle(self):
        return self.titleBar.windowTitle

    def get_layout(self):
        return self.__layout

    def get_message_box(self):
        return self.__message_box