import sys
import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Center import center_window

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
    def __init__(self, style="ghost", geometry=QRect(10, 10, 900, 520)):
        super().__init__() # set screen size (left, top, width, height

        self.setWindowFlags(Qt.FramelessWindowHint)
        
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(script_dir + os.path.sep + 'icons/phantom.png'))

        self.oldPos = self.pos()

        # self.__layout = QVBoxLayout()
        self.layout().setSpacing(0) 

        self.title_bar = phtm_title_bar(self, True)
        self.title_bar.generate_title_bar()

        self.addToolBar(Qt.TopToolBarArea, self.title_bar)

        self.setGeometry(geometry) # set screen size (left, top, width, height
        self.move(center_window(self))
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
            """)

class phtm_plain_text_edit(QPlainTextEdit):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style=style

        self.scroll_bar = QScrollBar()
        self.addScrollBarWidget(self.scroll_bar, Qt.AlignRight)

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
            self.scroll_bar.setStyleSheet("""
                QScrollBar:vertical {
                    width: 10px;
                    background: rgb(46, 51, 58);
                }

                QScrollBar::handle:vertical {
                    min-height: 5px;
                }

                QScrollBar::add-line:vertical {
                    background: none;
                    height: 45px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }

                QScrollBar::sub-line:vertical {
                    background: none;
                    height: 45px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }               

                QScrollBar::up-arrow:vertical { 
                    height: 3px; 
                    width: 3px 
                }

                QScrollBar::down-arrow:vertical {
                    height: 3px; 
                    width: 3px 
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

class phtm_dialog(QDialog):
    def __init__(self, title, geometry, central_dialog=None, style="ghost"):
        super().__init__() # set screen size (left, top, width, height

        # if not isinstance(central_dialog, QDialog):
        #     return "Pass central dialog is not of type QDialog"
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)

        self.__central_dialog = central_dialog

        self.style=style

        self.oldPos = self.pos()

        self.title_bar = phtm_title_bar(self)
        self.title_bar.generate_title_bar()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)

        self.__layout.addWidget(self.title_bar)
        if self.__central_dialog:
            self.__layout.addWidget(self.__central_dialog)

        self.setLayout(self.__layout)

        self.setGeometry(geometry)
        self.move(center_window(self))

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
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    color: white;
                }
                QMenuBar {
                    background-color: rgb(36, 143, 36);
                    color: rgb(217, 217, 217);
                }
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
                QMenuBar::item:selected {
                    background: rgb(17, 89, 17);
                }
                QLabel{
                    color: rgb(217, 217, 217);
                }
                QRadioButton {
                    color: rgb(217, 217, 217);
                }
                QRadioButton::indicator {
                    color: black;
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

    def get_layout(self):
        return self.__layout

    def set_central_dialog(self, dialog):
        # if not isinstance(central_dialog, QDialog):
        #    throw  "Pass central dialog is not of type QDialog"
        if not self.__central_dialog:
            self.__layout.addWidget(dialog)
        self.__central_dialog = dialog

    def central_dialog(self):
        return self.__central_dialog