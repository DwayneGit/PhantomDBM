import re

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from phtm_editor import phtm_editor
from style.phtm_main_window import phtm_main_window
from style.phtm_tab_widget import phtm_tab_widget
from file.json_script import json_script

class tab_widget(phtm_tab_widget):
    def __init__(self, parent=None):
        super().__init__()

        self.default_tab_count = 1

        self.parent = parent

        self.tab_data = {}

        if not isinstance(parent, QDialog):

            self.tabButton = QToolButton(self)
            self.tabButton.setText('+')
            self.tabButton.setObjectName("tab_button")

            font = self.tabButton.font()
            font.setBold(True)
            
            self.tabButton.setFont(font)
            self.setCornerWidget(self.tabButton)
            self.tabButton.clicked.connect(self.parent.add_defualt_script)

        self.tabBar().currentChanged.connect(lambda index: self.editWindowTitle(index))

    def editWindowTitle(self, index):
        # use regex to grab the name of the file from the path and added to title
        newTitle = self.parent.getPermanentTitle()
        # print(self.tabText(index))
        newTitle = self.tabText(index) + " - " + newTitle
        self.parent.parent.set_window_title(newTitle)
        self.parent.parent.currTitle = newTitle
        # print(newTitle)
