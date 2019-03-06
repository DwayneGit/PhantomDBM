import sys
import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

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
                    min-width: 10em;
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
                }
                QMenuBar {
                    background-color: rgb(36, 143, 36);
                    color: rgb(217, 217, 217);
                }
                QStatusBar {
                    background-color: rgb(92, 0, 153);
                    color: rgb(217, 217, 217);
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
                QComboBox:pressed {
                    background-color: rgb(39, 44, 51);
                    border-style: inset;
                }
                QComboBox::drop-down{
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    color: rgb(46, 51, 58);
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
                }
                QDialog {
                    background-color: rgb(64, 12, 96);
                }
                QDialog {
                    background-color: rgb(64, 12, 96);
                }
            """)

app = QApplication(sys.argv) #ignore()
window = phtm_main_window()
window.setWindowTitle("Hello World")
window.show()

# [Add widgets to the widget]

bttn = phtm_push_button("Button1")
pte = phtm_plain_text_edit()
pte.insertPlainText("ajfkldjaklfdjsafjdd")
cb=phtm_combo_box()
cb.addItems(['dsf','sdf','dfs'])
tb=phtm_tool_bar()
tbttn = QToolButton()
tbttn.setDefaultAction(QAction(QIcon("icons/load-file.png"),"open",window))
# tbload.triggered.connect()
tb.addWidget(tbttn)

# Put the widgets in a layout (now they start to appear):
layout = QGridLayout()

layout.addWidget(bttn, 0, 0)
layout.setRowStretch(2, 1)

layout.addWidget(pte, 1, 0)
layout.setRowStretch(2, 1)

layout.addWidget(cb, 2, 0)
layout.setRowStretch(2, 1)

window.addToolBar(tb)

window.menuBar().addMenu('File')

window.statusBar().showMessage("defaultMessage")

w = QWidget()
w.setLayout(layout)
window.setCentralWidget(w)

# [Resizing the window]
        
left = 10
top = 10
width = 900
height = 520
window.setGeometry(left, top, width, height)


# [Run the application]

# Start the event loop...
sys.exit(app.exec_())