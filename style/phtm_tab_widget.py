import re

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from phtm_editor import phtm_editor
from style.phtm_main_window import phtm_main_window

class phtm_tab_widget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.default_tab_count = 1

        self.parent = parent

        self.tab_data = {}

        if isinstance(parent, QMainWindow):

            self.tabButton = QToolButton(self)
            self.tabButton.setText('+')
            self.tabButton.setObjectName("tab_button")

            font = self.tabButton.font()
            font.setBold(True)
            
            self.tabButton.setFont(font)
            self.setCornerWidget(self.tabButton)
            self.tabButton.clicked.connect(self.add_editor)

        self.tabBar().currentChanged.connect(lambda index: self.editWindowTitle(index))
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

    def add_editor(self, editor=None):

        if editor:
            # print(editor.file_path)
            file_name = re.split('^(.+)\/([^\/]+)$', editor.file_path)
            self.addTab(editor, editor.title)

            editor.textChanged.connect( lambda: self.isChanged(self.currentIndex()))
            # self.editWindowTitle(self.currentIndex())

        else:
            default_tab = phtm_editor()
            default_tab.setPlainText("[\n    {\n        \"\": \"\"\n    }\n]")
            
            default_tab.title = "JSON Template"

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

    def editWindowTitle(self, index):
        # use regex to grab the name of the file from the path and added to title
        newTitle = self.parent.parent.getPermanentTitle()
        # print(self.tabText(index))
        newTitle = self.tabText(index) + " - " + newTitle
        self.parent.set_window_title(newTitle)
        self.parent.currTitle = newTitle
        # print(newTitle)

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
