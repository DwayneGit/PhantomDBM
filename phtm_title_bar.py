import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import style.style_template as styles   
    
class phtm_title_bar(styles.phtm_title_bar):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.is_max = False

    def generate_title_bar(self):

        self.setMovable( False )
        self.setFixedHeight(36)
        self.setIconSize(QSize(19, 19))

        exit_bttn = QToolButton()
        exit_bttn.setDefaultAction(QAction(QIcon("icons/window_icons/icons8-close-window-96.png"), "", self))
        exit_bttn.defaultAction().triggered.connect(sys.exit)
        self.addWidget(exit_bttn)

        screen_bttn = QToolButton()
        screen_bttn.setDefaultAction(QAction(QIcon("icons/window_icons/icons8-maximize-window-48.png"), "", self))
        screen_bttn.triggered.connect(lambda x : self.screen_toggle(screen_bttn))
        self.addWidget(screen_bttn)

        min_bttn = QToolButton()
        min_bttn.setDefaultAction(QAction(QIcon("icons/window_icons/icons8-minimize-window-48.png"), "", self))
        min_bttn.defaultAction().triggered.connect(self.main_window.showMinimized)
        self.addWidget(min_bttn)
    
    def screen_toggle(self, tool_button):
        if not self.is_max:
            self.main_window.showMaximized()
            tool_button.setDefaultAction(QAction(QIcon("icons/window_icons/icons8-restore-window-100.png"), "", self))
        elif self.is_max:
            self.main_window.showNormal()
            tool_button.setDefaultAction(QAction(QIcon("icons/window_icons/icons8-maximize-window-48.png"), "", self))

        self.is_max = not self.is_max

    def mousePressEvent(self, event):
        self.main_window.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.main_window.oldPos)
        #print(delta)
        self.main_window.move(self.main_window.x() + delta.x(), self.main_window.y() + delta.y())
        self.main_window.oldPos = event.globalPos()