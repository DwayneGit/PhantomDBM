from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class phtm_tool_bar(QToolBar):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style=style
        self.set_style()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QToolBar {
                    border-width: 0px;
                    background-color: rgb(46, 51, 58);
                }
                QToolButton {
                    border-width: 0px;
                    background-color: rgb(46, 51, 58);
                }
            """)