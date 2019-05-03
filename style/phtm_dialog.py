from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from style.phtm_title_bar import phtm_title_bar

from Center import center_window

class phtm_dialog(QDialog):
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

        self.style=style

        self.parent = parent

        self.oldPos = self.pos()

        self.title_bar = phtm_title_bar(self)
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
        self.set_style()

    def set_window_title(self, text):
        self.title_bar.set_window_title(text)
        self.setWindowTitle(text)
    
    def getWindowTitle(self):
        return self.title_bar.window_title

    def getPermanentTitle(self):
        return self.window_title

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QDialog {
                    background-color: rgb(46, 51, 58);
                    padding : 0px;
                    margin : 0px;
                }
                QLineEdit {
                    background-color: rgb(46, 51, 58);
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    color: white;
                }
                QMenuBar {
                    background-color: rgb(36, 143, 36);
                    color: rgb(217, 217, 217);
                }
                QMenuBar::item:selected {
                    background: rgb(17, 89, 17);
                }
                QLabel{
                    color: rgb(217, 217, 217);
                }
                QRadioButton {
                    color: rgb(217, 217, 217);
                }
                QRadioButton::indicator {
                    color: black;
                }
                QMenu {
                    background: rgb(36, 143, 36);
                    color: rgb(217, 217, 217);
                }
                QMenu::item:selected {
                    background: rgb(17, 89, 17);
                }
                QStatusBar {
                    background-color: rgb(92, 0, 153);
                    color: rgb(217, 217, 217);
                }
                QProgressBar {
                    background-color: rgb(92, 0, 153);
                }

                QProgressBar::chunk {
                    background-color: #05B8CC;
                    width: 10px;
                }
            """)

    def get_layout(self):
        return self.__layout

    def set_central_dialog(self, dialog):
        # if not isinstance(central_dialog, QDialog):
        #    throw  "Pass central dialog is not of type QDialog"
        if not self.__central_dialog:
            self.__layout.addWidget(dialog)
        self.__central_dialog = dialog

    def central_dialog(self):
        return self.__central_dialog