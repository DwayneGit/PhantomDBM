from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from phtm_editor import phtm_editor

class phtm_tab_widget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.default_tab_count = 1

        self.parent = parent

        self.tab_set_changed = {}

        self.tabButton = QToolButton(self)
        self.tabButton.setText('+')
        self.tabButton.setObjectName("tab_button")

        font = self.tabButton.font()
        font.setBold(True)

        self.tabButton.setFont(font)
        self.setCornerWidget(self.tabButton)
        self.tabButton.clicked.connect(self.add_editor)

        self.tabBar().currentChanged.connect(lambda index: self.editWindowTitle(index))
        
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

        self.setMovable(True)
        self.setTabsClosable(True)

        self.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        print(self.count())
        if self.count() <= 1:
            self.add_editor()
            self.removeTab(index)

        else:
            self.removeTab(index)

    def add_editor(self, editor=None, name=None):

        if editor:
            self.addTab(editor, name)

            editor.textChanged.connect( lambda: self.isChanged(self.currentIndex()))
            self.tab_set_changed[name] = False

        else:
            default_tab = phtm_editor()
            default_tab.setPlainText("[\n    {\n        \"\": \"\"\n    }\n]")
            
            default_name = "JSON Template"

            if default_name in self.tab_set_changed:
                default_name += " " + str(self.default_tab_count)

            self.default_tab_count += 1

            self.addTab(default_tab, default_name)

            default_tab.textChanged.connect( lambda x: self.isChanged(self.currentIndex()))
            self.tab_set_changed[default_name] = False

    def isChanged(self, index):
        if not self.tab_set_changed[self.get_tab_text(self.tabText(index))]:
            self.tab_set_changed[self.tabText(index)] = True
            self.setTabText(index,"* " + self.tabText(index))

    def editWindowTitle(self, index):
        # use regex to grab the name of the file from the path and added to title
        newTitle = self.parent.progTitle
        newTitle = self.tabText(index) + " - " + newTitle
        self.parent.setWindowTitle(newTitle)
        self.parent.currTitle = newTitle
        print(newTitle)

    def get_tab_text(self, text):
        # print(text[0:2])
        if text[0:2] == "* ":
            # print(text[2:])
            return text[2:]
        else: return text
