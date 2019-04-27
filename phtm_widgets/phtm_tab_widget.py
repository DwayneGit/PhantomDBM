import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTabWidget, QMessageBox

from phtm_editor import phtm_editor
from phtm_widgets.phtm_main_window import phtm_main_window
from file.json_script import json_script

class phtm_tab_widget(QTabWidget):
    clearTabsRequested = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.default_tab_count = 1
        self.tab_data = {}
        self.script_set = {}

        self.set_style()

        self.tabCloseRequested.connect(self.close_tab)

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

    def tab_by_text(self, text):
        tabIndexFound = -1
        for i in range( self.count()):
            if text == self.tabText(i):
                tabIndexFound = i
                self.setCurrentIndex(i)
                break
        # print(tabIndexFound)
        return tabIndexFound

    def close_tab(self, index):
        if self.widget(index).is_changed:
            save_msg = "The current script is not saved. Are you Sure you want to close?"
            reply = QMessageBox.question(self, 'Message', 
                            save_msg, QMessageBox.Yes | QMessageBox.Save | QMessageBox.Cancel, QMessageBox.Cancel)

            if reply == QMessageBox.Cancel:
                return
            elif reply == QMessageBox.Save:
                self.widget(index).save_script()
            elif reply == QMessageBox.Yes:
                self.is_saved(self.tabText(index)[2:], index)
                
        self.removeTab(index)
        if self.count() < 1:
            self.hide()

    def clear(self):
        for index in range(self.count()):
            self.tabCloseRequested.emit(0)

    def add_editor(self, script=None):
        if script:
            editor = phtm_editor(script)
            
            file_name = script.get_title()
            index = self.addTab(editor, editor.title)

            editor.textChanged.connect(lambda: self.isChanged(self.currentIndex()))
            editor.saved.connect(lambda title: self.is_saved(title, self.currentIndex()))

        else:
            editor = phtm_editor()
            index = self.addTab(editor, "")
            editor.textChanged.connect(lambda: self.isChanged(self.currentIndex()))
            editor.saved.connect(lambda title: self.is_saved(title, self.currentIndex()))

        self.setCurrentIndex(index)
        return index

    def is_saved(self, title, index):
        self.widget(index).is_changed = False
        self.setTabText(index, title)

        self.widget(index).get_tree_item().setText(0, title)
        
    def isChanged(self, index):
        if not self.widget(index).is_changed and self.tabText(index):
            self.widget(index).is_changed = True
            self.setTabText(index, "* " + self.tabText(index))

            self.widget(index).get_tree_item().setText(0, self.tabText(index))

    def get_index(self, editor):
        return self.indexOf(editor)

    def get_tab_text(self, index):
        if self.tabText(index)[0:2] == "* ":
            return self.tabText(index)[2:]
        else: return self.tabText(index)
