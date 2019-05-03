import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from phantom.utility import center_window

from phantom.application_settings import settings
from phantom.core import main_window

from . import PhtmTitleBar

class PhtmMainWindow(QMainWindow):
    def __init__(self, geometry=QRect(10, 10, 1100, 620)):
        super().__init__() # set screen size (left, top, width, height

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("pmainwind")

        self.__program_title = "Phantom DBM"
        self.window_title = ''

        self.setWindowIcon(QIcon("icons/phantom.png"))
        self.oldPos = self.pos()

        self.layout().setSpacing(0)

        self.title_bar = PhtmTitleBar(self, True)
        self.title_bar.generate_title_bar()

        self.set_window_title(self.__program_title)

        self.addToolBar(Qt.TopToolBarArea, self.title_bar)

        self.setGeometry(geometry) # set screen size (left, top, width, height
        self.move(center_window(self))

        self.setCentralWidget(main_window(self))

    def getPermanentTitle(self):
        return self.__program_title

    def getWindowTitle(self):
        return self.title_bar.window_title

    def set_window_title(self, text):
        self.title_bar.set_window_title(text)
        self.setWindowTitle(text)
