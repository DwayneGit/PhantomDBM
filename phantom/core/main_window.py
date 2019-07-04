from copy import deepcopy
import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect, Qt, QCoreApplication, pyqtSlot, QFileInfo
from PyQt5.QtWidgets import QMainWindow, QSplitter, QProgressBar, QMessageBox, QWidget, QHBoxLayout, QAction, QVBoxLayout

from phantom.users import loginScreen
from phantom.database import DatabaseHandler
from phantom.utility import center_window

from phantom.preferences import preference_body
from phantom.application_settings import settings

from phantom.phtm_widgets import PhtmDialog, PhtmPlainTextEdit, PhtmTitleBar

from phantom.file_stuff import FileHandler

from . import run_ctrl
from . import phtm_menu_bar
from . import main_tool_bar
from . import PhtmEditorWidget

BUFFERSIZE = 1000

class main_window(QMainWindow):
    runs = 0
    completed_run_counter = 0
    def __init__(self, parent=None):
        super().__init__()

        settings.__LOG__.logInfo("Program Started.")
        self.setObjectName("pmainwind")

        self.user = None
        self.changed = False
        self.filePath = None
        self.fileLoaded = True
        self.window_title = ''
        self.dmi_settings = None
        self.__editor_widget = None

        self.title_bar = PhtmTitleBar(self, True)
        self.title_bar.generate_title_bar()

        self.__program_title = "Phantom DBM"
        self.set_window_title(self.__program_title)

        self.oldPos = self.pos()
        self.setWindowIcon(QIcon("icons/logo.png"))

        self.setGeometry(QRect(10, 10, 1100, 620)) # left, top, width, height
        self.move(center_window(self))

        self.layout().setSpacing(0)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.addToolBar(Qt.TopToolBarArea, self.title_bar)

        self.r_ctrl = run_ctrl(self)

        self.body = QMainWindow()
        self.setCentralWidget(self.body)

        self.file_handler = FileHandler(self)
        self.file_handler.tmpScriptCleaner()
        login = PhtmDialog("Login", QRect(10, 10, 260, 160), self)
        login.set_central_dialog(loginScreen(login))

        self.__initUI()

        # if login.exec_():
        #     settings.__LOG__.logInfo("Successfully Logged In.")
        #     self.user = login.get_central_dialog().user
        #     self.initUI()
        # else:
        #     settings.__LOG__.logInfo("No login program exited.")
        #     sys.exit()

    def __initUI(self):

        self.currTitle = self.window_title

        self.__brd_widget = QWidget()
        self.__brd_widget_lay = QHBoxLayout()

        self.__brd = PhtmPlainTextEdit()
        self.__brd.setReadOnly(True)
        self.__brd.insertPlainText("Welcome to Phantom Database Manager (DBM).")

        self.__brd_widget_lay.addWidget(self.__brd)
        self.__brd_widget_lay.setContentsMargins(0, 0, 0, 0)

        self.__brd_widget.setLayout(self.__brd_widget_lay)
        self.__brd.setObjectName("brd")

        self.__editor_widget = PhtmEditorWidget(self.file_handler, self)

        self.__splitter1 = QSplitter(Qt.Horizontal)
        self.__splitter1.addWidget(self.__brd_widget)
        self.__splitter1.addWidget(self.__editor_widget)
        self.__splitter1.setHandleWidth(1)
        self.__splitter1.setSizes([300, 325])

        self.body.setCentralWidget(self.__splitter1)
        
        self.body.statusBar().showMessage('Ready')
        self.body.statusBar().setFixedHeight(20)

        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)

        self.body.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setFixedWidth(200)

        self.main_tool_bar = main_tool_bar(self.file_handler, self)
        self.main_tool_bar.setUpToolBar()

        self.menu_bar = phtm_menu_bar(self.file_handler, self)
        self.menu_bar.init_menu_bar()
        self.file_handler.set_adjust_signal(self.menu_bar.get_adjust_signal())

        self.body.setMenuWidget(self.menu_bar)

        self.show()

    def set_window_title(self, text):
        self.title_bar.set_window_title(text)
        self.setWindowTitle(text)

    def getWindowTitle(self):
        return self.getWindowTitle()

    def updateWindowTitle(self, newTitle):
        self.set_window_title(newTitle + " - " + self.getPermanentTitle())

    def get_main_toolbar(self):
        return self.main_tool_bar

    def get_menubar(self):
        return self.menu_bar

    def getPermanentTitle(self):
        return self.__program_title

    @pyqtSlot(str)
    def appendToBoard(self, message):
        # settings.__LOG__.logInfo(message)
        self.__brd.appendHtml(message)
        QCoreApplication.processEvents()

    def closeEvent(self, event):
        if self.changed:
            quit_msg = "Your changes have not been saved.\nAre you sure you want to exit the program?"
            reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            settings.__LOG__.logInfo("Program Ended")

    def showPref(self, index=0):
        pref_dialog = preference_body(self.get_editor_widget().get_cluster(), self.user)
        pref_dialog.tabW.setCurrentIndex(index)

        if pref_dialog.exec_():
            self.reload_curr_dmi()
            self.reloadDbNames()

    def reloadDbNames(self):
        self.main_tool_bar.dbnameMenu.currentTextChanged.disconnect()
        self.main_tool_bar.dbnameMenu.clear()

        self.main_tool_bar.dbnameMenu.addItems(DatabaseHandler.getDatabaseList(settings.__DATABASE__.get_host_name(), settings.__DATABASE__.get_port_number()))
        self.main_tool_bar.dbnameMenu.currentTextChanged.connect(self.main_tool_bar.databaseNameChanged)

        index = self.main_tool_bar.dbnameMenu.findText(settings.__DATABASE__.get_database_name())
        self.main_tool_bar.dbnameMenu.setCurrentIndex(index)

    def reload_curr_dmi(self):
        self.main_tool_bar.curr_dmi.setPlainText(self.get_editor_widget().get_cluster().get_phm_scripts()["__dmi_instr__"]["name"])

    def get_editor_widget(self):
        return self.__editor_widget

    def new_editor_widget(self):
        if self.file_handler.save_phm(self.menu_bar.get_adjust_signal()):
            new_ew = PhtmEditorWidget(self)
            self.__splitter1.replaceWidget(self.__splitter1.indexOf(self.__editor_widget), new_ew)
            self.__editor_widget = new_ew
            self.main_tool_bar.dbnameMenu.setCurrentIndex(0)
