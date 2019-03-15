import sys
import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from style.phtm_title_bar import phtm_title_bar

from Center import center_window

class phtm_main_window(QMainWindow):
    def __init__(self, style="ghost", geometry=QRect(10, 10, 900, 520)):
        super().__init__() # set screen size (left, top, width, height

        self.setWindowFlags(Qt.FramelessWindowHint)
        
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(script_dir + os.path.sep + 'icons/phantom.png'))

        self.oldPos = self.pos()

        # self.__layout = QVBoxLayout()
        self.layout().setSpacing(0) 

        self.title_bar = phtm_title_bar(self, True)
        self.title_bar.generate_title_bar()

        self.addToolBar(Qt.TopToolBarArea, self.title_bar)

        self.setGeometry(geometry) # set screen size (left, top, width, height
        self.move(center_window(self))
        self.style=style
        self.set_style()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: rgb(46, 51, 58);
                    padding : 0px;
                }
                QMenuBar {
                    background-color: rgb(36, 143, 36);
                    color: rgb(217, 217, 217);
                }
                QMenuBar::item:selected {
                    background: rgb(17, 89, 17);
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
                QTabWidget::pane {
                    background-color: rgb(46, 51, 58);
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    color: rgb(217, 217, 217);
                }
                QTabBar::tab {
                    background: rgb(39, 44, 51);
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    color: rgb(217, 217, 217);
                    min-width: 8ex;
                    padding: 2px;
                }
            """)