import sys
import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class phtm_icons():
    def __init__(self, path="icons/standard_white/"):
        self.get_icons(path)

    def get_icons(self, path):
        self.play = path+"play.png"
        self.save = path+"save.png"
        self.stop = path+"stop.png"
        self.edit = path+"edit.png"
        self.wifi = path+"wifi.png"
        self.settings = path+"settings.png"
        self.load_file = path+"load-file.png"
        self.import_file = path+"import-file.png"
        self.export_file = path+"export-file.png"

class phtm_push_button(QPushButton):
    def __init__(self, text, parent=None, style="ghost"):
        super().__init__(text, parent)
        self.setFlat(True)
        self.style=style
        self.set_style()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgb(46, 51, 58);
                    color: rgb(217, 217, 217);
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    font: bold 14px;
                    padding: 6px;
                }
                QPushButton:pressed {
                    background-color: rgb(39, 44, 51);
                    border-style: inset;
                }
            """)

class phtm_main_window(QMainWindow):
    def __init__(self, style="ghost"):
        super().__init__() # set screen size (left, top, width, height
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
            """)

class phtm_plain_text_edit(QPlainTextEdit):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style=style
        self.set_style()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QPlainTextEdit {
                    background-color: rgb(46, 51, 58);
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    color: white;
                }
            """)

class phtm_text_edit(QTextEdit):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style=style
        self.set_style()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QTextEdit {
                    background-color: rgb(46, 51, 58);
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    color: white;
                }
            """)


class phtm_combo_box(QComboBox):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style=style
        self.set_style()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QComboBox {
                    background-color: rgb(46, 51, 58);
                    color: rgb(217, 217, 217);
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    font: bold 14px;
                    min-width: 10em;
                    padding: 6px;
                }
                QComboBox::drop-down{
                    border-style: outset;
                    border-width: 0px;
                    border-color: rgb(39, 44, 51);
                    color: rgb(46, 51, 58);
                    padding: 0px;
                }
                QComboBox::item{
                    background-color: rgb(46, 51, 58);
                    color: rgb(217, 217, 217);
                }
                QComboBox::item::selected{
                    background-color: rgb(39, 44, 51);
                }
            """)

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

class phtm_title_bar(QToolBar):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style=style
        self.set_style()

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

class phtm_dialog(QDialog):
    def __init__(self, style="ghost"):
        super().__init__() # set screen size (left, top, width, height
        self.style=style
        self.set_style()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QDialog {
                    background-color: rgb(46, 51, 58);
                    padding : 0px;
                    margin : 0px;
                }
                QLineEdit {
                    background-color: rgb(46, 51, 58);
                    color: rgb(217, 217, 217);
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
            """)