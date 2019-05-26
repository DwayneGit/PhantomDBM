from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QInputDialog, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from phantom.utility import center_window

from . import PhtmTitleBar

class PhtmInputDialog(QDialog):
    def __init__(self, parent, title, msg, echo_mode, text=None):
        super().__init__(parent) # set screen size (left, top, width, height

        # if not isinstance(central_dialog, QDialog):
        #     return "Pass central dialog is not of type QDialog"
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowModality(Qt.ApplicationModal)

        self.window_title = title

        self.parent = parent

        self.oldPos = self.pos()

        self.title_bar = PhtmTitleBar(self)
        self.title_bar.generate_title_bar()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)

        self.__layout.addWidget(self.title_bar)
        self.__input_dialog = QInputDialog()

        self.selected_value = None
        if msg:
            self.__input_dialog.setLabelText(msg)
        self.__input_dialog.setTextEchoMode(echo_mode)

        self.__input_dialog.textValueSelected.connect(self.value_selected)
        self.__input_dialog.rejected.connect(self.reject)

        self.__layout.addWidget(self.__input_dialog)

        self.setLayout(self.__layout)

        # self.setGeometry(geometry)
        # self.move(center_window(self))

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(30, 30, 30))
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3)
        self.setGraphicsEffect(self.shadow)

        self.set_window_title(self.window_title)

    def value_selected(self, value):
        self.selected_value = value
        self.accept()

    def set_window_title(self, text):
        self.title_bar.set_window_title(text)
        self.setWindowTitle(text)
    
    def getWindowTitle(self):
        return self.title_bar.window_title

    def get_layout(self):
        return self.__layout

    def get_input_dialog(self):
        return self.__input_box