from copy import deepcopy

from PyQt5.QtCore import QRect, Qt, QCoreApplication, pyqtSlot, QFileInfo
from PyQt5.QtWidgets import QMainWindow, QSplitter, QProgressBar, QMessageBox, QWidget, QHBoxLayout, QAction

from phantom.users import loginScreen
from phantom.database import DatabaseHandler

import phantom.preferences as prefs
from phantom.application_settings import settings

from phantom.phtm_widgets import PhtmDialog, PhtmPlainTextEdit

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
        settings.__LOG__.logInfo("Program Started.")
        self.dmi_settings = None
        self.prefs = None
        self.dbData = None

        self.maxFileNum = 4
        self.recentFileActionList = []
        self.createActionsAndConnections()

        self.currentFile = None

        self.r_ctrl = run_ctrl(self)

        self.user = None

        f_ctrl.tmpScriptCleaner(self)
        login = PhtmDialog("Login", QRect(10, 10, 260, 160), self)
        login.set_central_dialog(loginScreen(login))
        self.__editor_widget = None
        self.__initUI()

        # if login.exec_():
        #     settings.__LOG__.logInfo("Successfully Logged In.")
        #     self.user = login.get_central_dialog().user
        #     self.initUI()
        # else:
        #     settings.__LOG__.logInfo("No login program exited.")
        #     sys.exit()

    def __initUI(self):
        '''
        initiates application UI
		'''
        self.currTitle = self.parent.window_title

        self.__splitter1 = QSplitter(Qt.Horizontal)

        # Add text field
        self.__brd_widget = QWidget()
        self.__brd_widget_lay = QHBoxLayout()

        self.__brd = PhtmPlainTextEdit()
        self.__brd.setReadOnly(True)
        self.__brd.insertPlainText("Welcome to Phantom Database Manager (DBM).")

        self.__brd_widget_lay.addWidget(self.__brd)
        self.__brd_widget_lay.setContentsMargins(0, 0, 0, 0)

        self.__brd_widget.setLayout(self.__brd_widget_lay)
        self.__brd.setObjectName("brd")

        self.fileLoaded = True
        self.filePath = None

        self.__editor_widget = PhtmEditorWidget(self)

        self.load_settings()

        # settings.__DATABASE__ = DatabaseHandler(self.dbData)

        self.changed = False
        # check if file is loaded and set flag to use to ask if save necessary before running or closing
        self.__splitter1.addWidget(self.__brd_widget)
        self.__splitter1.addWidget(self.__editor_widget)
        self.__splitter1.setHandleWidth(1)

        self.setCentralWidget(self.__splitter1)

        self.__splitter1.setSizes([300, 325])
        # self.setStatusBar(StatusBar())
        self.statusBar().showMessage('Ready')
        self.statusBar().setFixedHeight(20)

        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)

        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setFixedWidth(200)

        self.main_tool_bar = main_tool_bar(self)
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
        # settings.__LOG__.logInfo(message)
        self.__brd.appendHtml(message)
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
            settings.__LOG__.logInfo("Program Ended")

    def showPref(self, index=0):
        p = PhtmDialog("Preferences", QRect(10, 10, 450, 500), self)
        p.set_central_dialog(prefs.preference_body(self.user, p))
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
        
        self.main_tool_bar.dbnameMenu.addItems(DatabaseHandler.getDatabaseList(self.dbData['host'], self.dbData['port']))
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
        if f_ctrl.save_phm(self.__editor_widget, self.adjustForCurrentFile):
            new_ew = PhtmEditorWidget(self)
            self.__splitter1.replaceWidget(self.__splitter1.indexOf(self.__editor_widget), new_ew)
            self.__editor_widget = new_ew
            self.main_tool_bar.dbnameMenu.setCurrentIndex(0)

    def adjustForCurrentFile(self, filePath):

        recentFilePaths = settings.__APPLICATION_SETTINGS__.get_settings()['recent_files']

        try:
            recentFilePaths.remove(filePath)
        except Exception as err:
            settings.__LOG__.logError(str(err))

        recentFilePaths.insert(0, filePath)

        while len(recentFilePaths) > self.maxFileNum:
            recentFilePaths.pop()

        self.updateRecentActionList()

    def updateRecentActionList(self):

        recentFilePaths = settings.__APPLICATION_SETTINGS__.get_settings()['recent_files']

        itEnd = 0
        if len(recentFilePaths) <= self.maxFileNum:
            itEnd = len(recentFilePaths)
        else:
            itEnd = self.maxFileNum
        
        for i in range(0, itEnd):
            strippedName = QFileInfo(recentFilePaths[i]).fileName()
            self.recentFileActionList[i].setText(strippedName)
            self.recentFileActionList[i].setData(recentFilePaths[i])
            self.recentFileActionList[i].setVisible(True)

        for j in range(itEnd, self.maxFileNum):
            self.recentFileActionList[j].setVisible(False)

        settings.__APPLICATION_SETTINGS__.update_settings()

    def createActionsAndConnections(self):
        recentFileAction = None
        for i in range(0, self.maxFileNum):
            recentFileAction = QAction(self.parent)
            recentFileAction.setVisible(False)
            recentFileAction.triggered.connect(self.openRecent)

            self.recentFileActionList.append(recentFileAction)

    def openRecent(self):
        if not f_ctrl.load_phm(self, self.sender().data()):
            recentFilePaths = settings.__APPLICATION_SETTINGS__.get_settings()['recent_files']

            try:
                recentFilePaths.remove(self.sender().data())
            except Exception as err:
                settings.__LOG__.logError("IOError: " + str(err))

            self.updateRecentActionList()