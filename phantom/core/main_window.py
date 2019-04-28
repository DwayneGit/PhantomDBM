from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect, Qt, QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QSplitter, QProgressBar, QMessageBox

from phantom.users import loginScreen
from phantom.database import database_handler

import phantom.preferences as prefs

from phantom.logging_stuff import phtm_logger
from phantom.phtm_widgets import PhtmIcons
from phantom.phtm_widgets import PhtmDialog
from phantom.phtm_widgets import PhtmPlainTextEdit

from phantom.file_stuff import file_ctrl as f_ctrl

from . import run_ctrl
from . import phtm_menu_bar
from . import main_tool_bar, databaseNameChanged
from . import PhtmEditorWidget

BUFFERSIZE = 1000

class main_window(QMainWindow):
    runs = 0
    completed_run_counter = 0
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.log = phtm_logger()
        self.log.logInfo("Program Started.")
        self.dmi_settings = None
        self.prefs = None
        self.dbData = None

        self.r_ctrl = run_ctrl(self)

        self.user = None
        self.icon_set = PhtmIcons()

        f_ctrl.tmpScriptCleaner(self)
        login = PhtmDialog("Login", QRect(10, 10, 260, 160), self)
        login.set_central_dialog(loginScreen(login))
        self.__editor_widget = None
        self.initUI()

        # if login.exec_():
        #     self.log.logInfo("Successfully Logged In.")
        #     self.user = login.get_central_dialog().user
        #     self.initUI()
        # else:
        #     self.log.logInfo("No login program exited.")
        #     sys.exit()

    def initUI(self):
        '''
        initiates application UI
		'''
        self.currTitle = self.parent.window_title

        self.parent.setWindowIcon(QIcon('icons/phantom.png'))

        self.__splitter1 = QSplitter(Qt.Horizontal)


        # Add text field
        self.brd = PhtmPlainTextEdit()
        self.brd.setReadOnly(True)
        self.brd.insertPlainText("Welcome to Phantom Database Manager (DBM).")

        self.fileLoaded = True
        self.filePath = None

        self.__editor_widget = PhtmEditorWidget(self)

        self.load_settings()

        self.changed = False
        # check if file is loaded and set flag to use to ask if save necessary before running or closing
        self.__splitter1.addWidget(self.brd)
        self.__splitter1.addWidget(self.__editor_widget)

        self.setCentralWidget(self.__splitter1)

        self.__splitter1.setSizes([300, 325])
        # self.setStatusBar(StatusBar())
        self.statusBar().showMessage('Ready')
        self.statusBar().setFixedHeight(20)

        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)

        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setFixedWidth(200)

        self.main_tool_bar = main_tool_bar(self, self.icon_set)
        self.main_tool_bar.setUpToolBar()

        self.menu_bar = phtm_menu_bar(self)
        self.menu_bar.init_menu_bar()

        self.setMenuWidget(self.menu_bar)

        self.show()

    def set_window_title(self, text):
        self.parent.set_window_title(text)

    def getWindowTitle(self):
        return self.parent.getWindowTitle()

    def updateWindowTitle(self, newTitle):
        self.set_window_title(newTitle + " - " + self.parent.getPermanentTitle())

    def get_main_toolbar(self):
        return self.main_tool_bar

    #create custom signal to ubdate UI
    @pyqtSlot(str)
    def appendToBoard(self, message, msg_type = 0):
        # self.log.logInfo(message)
        self.brd.appendHtml(message)
        QCoreApplication.processEvents()

    def closeEvent(self, event):
        if self.changed:
            quit_msg = "Your changes have not been saved.\nAre you sure you want to exit the program?"
            reply = QMessageBox.question(self, 'Message', 
                            quit_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            self.log.logInfo("Program Ended")

    def showPref(self, index=0):
        p = PhtmDialog("Preferences", QRect(10, 10, 350, 475), self)
        p.set_central_dialog(prefs.preference_body(self.user, self.log, p))
        p.get_central_dialog().tabW.setCurrentIndex(index)

        if p.exec_():
            self.prefs = p.prefs
            self.dbData = self.prefs['mongodb']
            self.reload_curr_dmi()
            self.reloadDbNames()

        else:
            pass

    def reloadDbNames(self):
        self.main_tool_bar.dbnameMenu.currentTextChanged.disconnect()
        self.main_tool_bar.dbnameMenu.clear()
        
        self.main_tool_bar.dbnameMenu.addItems(database_handler.getDatabaseList(self.dbData['host'], self.dbData['port'], self.log))
        self.main_tool_bar.dbnameMenu.currentTextChanged.connect(lambda: databaseNameChanged(self.main_tool_bar, self))

        index = self.main_tool_bar.dbnameMenu.findText(self.prefs['mongodb']['dbname'])
        self.main_tool_bar.dbnameMenu.setCurrentIndex(index)

    def load_settings(self):
        self.prefs = self.__editor_widget.get_cluster().get_settings()
        self.dbData = self.prefs['mongodb']

    def reload_curr_dmi(self):
        self.main_tool_bar.curr_dmi.setPlainText(self.get_editor_widget().get_cluster().get_phm_scripts()["__dmi_instr__"]["name"])

    def get_editor_widget(self):
        return self.__editor_widget

    def new_editor_widget(self):
        new_ew = PhtmEditorWidget(self)
        self.__splitter1.replaceWidget(self.__splitter1.indexOf(self.__editor_widget), new_ew)
        self.__editor_widget = new_ew
        self.main_tool_bar.dbnameMenu.setCurrentIndex(0)
