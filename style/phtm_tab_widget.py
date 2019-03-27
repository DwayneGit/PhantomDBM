import re

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from phtm_editor import phtm_editor
from style.phtm_main_window import phtm_main_window
from file.json_script import json_script

class phtm_tab_widget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.default_tab_count = 1
        self.parent = parent

        self.tab_data = {}

        self.set_style()

    def set_style(self):

        self.setStyleSheet('''
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
            QToolButton#tab_button {
                background-color: rgb(46, 51, 58);
                color: rgb(217, 217, 217);
                border-style: none;
                border-width: 1px;
                border-color: rgb(46, 51, 58);
                font: bold 14px;
                padding: 6px;
            }
            QToolButton#tab_button:pressed {
                background-color: rgb(39, 44, 51);
                border-style: inset;
            }
        ''')

        self.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        # print(self.count())
        if self.count() <= 1:
            self.add_editor()
            self.removeTab(index)

        else:
            self.removeTab(index)

    def add_editor(self, script=None):

        if script:
            editor = phtm_editor(script)
            # print(editor.file_path)
            
            file_name = script.get_title()
            self.addTab(editor, editor.title)

            editor.textChanged.connect( lambda: self.isChanged(self.currentIndex()))
            # self.editWindowTitle(self.currentIndex())

        else:
            default_tab = phtm_editor(json_script("[\n    {\n        \"\": \"\"\n    }\n]", "JSON Template"))

            for index in range(self.count()):
                if default_tab.title == self.tabText(index):
                    default_tab.title += " " + str(self.default_tab_count)

            self.default_tab_count += 1

            self.addTab(default_tab, default_tab.title)

            default_tab.textChanged.connect( lambda: self.isChanged(self.currentIndex()))
            # self.editWindowTitle(self.currentIndex())

    def isChanged(self, index):
        if not self.widget(index).is_changed:
            self.widget(index).is_changed = True
            self.setTabText(index, "* " + self.tabText(index))

    def get_index(self, editor):
        return self.indexOf(editor)

    def get_tab_text(self, index):
        # print(text[0:2])
        if self.tabText(index)[0:2] == "* ":
            # print(text[2:])
            return self.tabText(index)[2:]
        else: return self.tabText(index)

    def editTabTitle(self, title):
        self.setTabText(self.currentIndex(), title)
        # print(self.tabText(self.currentIndex()))
