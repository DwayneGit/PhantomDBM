from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout

from phantom.utility import center_window

from . import PhtmTitleBar

class PhtmDialog(QDialog):
    def __init__(self, title, geometry, parent, central_dialog=None, style="ghost"):
        super().__init__() # set screen size (left, top, width, height

        # if not isinstance(central_dialog, QDialog):
        #     return "Pass central dialog is not of type QDialog"
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowModality(Qt.ApplicationModal)

        self.__central_dialog = central_dialog

        self.window_title = title

        self.parent = parent

        self.oldPos = self.pos()

        self.title_bar = PhtmTitleBar(self)
        self.title_bar.generate_title_bar()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)

        self.__layout.addWidget(self.title_bar)
        if self.__central_dialog:
            self.__layout.addWidget(self.__central_dialog)

        self.setLayout(self.__layout)

        self.setGeometry(geometry)
        self.move(center_window(self))

        self.set_window_title(self.window_title)

    def set_window_title(self, text):
        self.title_bar.set_window_title(text)
        self.setWindowTitle(text)
    
    def getWindowTitle(self):
        return self.title_bar.window_title

    def get_layout(self):
        return self.__layout

    def set_central_dialog(self, dialog):
        # if not isinstance(central_dialog, QDialog):
        #    throw  "Pass central dialog is not of type QDialog"
        if not self.__central_dialog:
            self.__layout.addWidget(dialog)
        self.__central_dialog = dialog

    def get_central_dialog(self):
        return self.__central_dialog