import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class phtm_title_bar(QToolBar):
    def __init__(self, window, is_main_window=False, style="ghost"):
        super().__init__()
        self.style=style
        self.window = window
        self.is_max = False
        self.is_main_window = is_main_window
        self.set_style()

    def generate_title_bar(self):

        self.setMovable( False )
        self.setFixedHeight(36)
        self.setIconSize(QSize(19, 19))

        exit_bttn = QToolButton()
        exit_bttn.setDefaultAction(QAction(QIcon("icons/window_icons/icons8-close-window-96.png"), "", self))

        if self.is_main_window:
            logo_bttn = QToolButton()
            logo_bttn.setDefaultAction(QAction(QIcon("icons/phantom.png"), "PhantomDBM", self))
            logo_bttn.setObjectName("logo")
            self.addWidget(logo_bttn)

            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.addWidget(spacer)

            min_bttn = QToolButton()
            min_bttn.setDefaultAction(QAction(QIcon("icons/window_icons/icons8-minimize-window-48.png"), "", self))
            min_bttn.defaultAction().triggered.connect(self.window.showMinimized)
            self.addWidget(min_bttn)

            screen_bttn = QToolButton()
            screen_bttn.setDefaultAction(QAction(QIcon("icons/window_icons/icons8-maximize-window-48.png"), "", self))
            screen_bttn.triggered.connect(lambda x : self.screen_toggle(screen_bttn))
            self.addWidget(screen_bttn)

            exit_bttn.defaultAction().triggered.connect(sys.exit)
            exit_bttn.setObjectName("exit")

        else:
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.addWidget(spacer)

            exit_bttn.defaultAction().triggered.connect(self.window.close)
            exit_bttn.setObjectName("exit")
        
        self.addWidget(exit_bttn)
    
    def screen_toggle(self, tool_button):
        if not self.is_max:
            self.window.showMaximized()
            tool_button.setDefaultAction(QAction(QIcon("icons/window_icons/icons8-restore-window-100.png"), "", self))
        elif self.is_max:
            self.window.showNormal()
            tool_button.setDefaultAction(QAction(QIcon("icons/window_icons/icons8-maximize-window-48.png"), "", self))

        self.is_max = not self.is_max

    def mousePressEvent(self, event):
        self.window.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.window.oldPos)
        #print(delta)
        self.window.move(self.window.x() + delta.x(), self.window.y() + delta.y())
        self.window.oldPos = event.globalPos()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QToolBar {
                    background-color: rgb(92, 0, 153);
                    color: rgb(217, 217, 217);
                    border-style: outset;
                    border-radius: 0px;
                    border: 0px;
                }
                QToolButton {
                    background-color: rgb(92, 0, 153);
                    border-width: 0px;
                }
                QToolButton:hover {
                    background-color: rgb(81, 0, 135);
                    border-width: 0px;
                    border-style: outset;
                    border-radius: 0px;
                    border: 0px;
                }
                QToolButton#logo:hover  {
                    background-color: rgb(92, 0, 153);
                    border: 0px;
                }
                QToolButton#exit:hover  {
                    background-color: red;
                    border: 0px;
                }
            """)