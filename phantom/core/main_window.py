from copy import deepcopy
import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect, Qt, QCoreApplication, pyqtSlot, QFileInfo
from PyQt5.QtWidgets import QMainWindow, QSplitter, QProgressBar, QMessageBox, QWidget, QHBoxLayout, QAction, QVBoxLayout

from phantom.users import loginScreen
from phantom.database import DatabaseHandler
from phantom.utility import centerWindow

from phantom.preferences import PreferenceBody
from phantom.applicationSettings import settings

from phantom.phtmWidgets import PhtmDialog, PhtmPlainTextEdit, PhtmTitleBar

from phantom.file_stuff import FileHandler

from . import RunCtrl
from . import PhtmMenuBar
from . import MainToolBar
from . import PhtmEditorWidget

BUFFERSIZE = 1000

class MainWindow(QMainWindow):
    runs = 0
    completedRunCounter = 0
    def __init__(self, parent=None):
        super().__init__()

        settings.__LOG__.logInfo("Program Started.")
        self.setObjectName("pmainwind")

        self.user = None
        self.changed = False
        self.filePath = None
        self.fileLoaded = True
        self.windowTitle = ''
        self.DmiSettings = None
        self.__editorWidget = None

        self.titleBar = PhtmTitleBar(self, True)
        self.titleBar.generateTitleBar()

        self.__programTitle = "Phantom DBM"
        self.setWindowTitle(self.__programTitle)

        self.oldPos = self.pos()
        self.setWindowIcon(QIcon("icons/logo.png"))

        self.setGeometry(QRect(10, 10, 1100, 620)) # left, top, width, height
        self.move(centerWindow(self))

        self.layout().setSpacing(0)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.addToolBar(Qt.TopToolBarArea, self.titleBar)

        self.r_ctrl = RunCtrl(self)

        self.body = QMainWindow()
        self.setCentralWidget(self.body)

        self.fileHandler  = FileHandler(self)
        login = PhtmDialog("Login", QRect(10, 10, 260, 160), self)
        login.setCentralDialog(loginScreen(login))

        self.__initUI()

        # if login.exec_():
        #     settings.__LOG__.logInfo("Successfully Logged In.")
        #     self.user = login.get_central_dialog().user
        #     self.initUI()
        # else:
        #     settings.__LOG__.logInfo("No login program exited.")
        #     sys.exit()

    def __initUI(self):

        self.currTitle = self.windowTitle

        self.__boardWidget = QWidget()
        self.__boardWidgetLayout = QHBoxLayout()

        self.__brd = PhtmPlainTextEdit()
        self.__brd.setReadOnly(True)
        self.__brd.insertPlainText("Welcome to Phantom Database Manager (DBM).")

        self.__boardWidgetLayout.addWidget(self.__brd)
        self.__boardWidgetLayout.setContentsMargins(0, 0, 0, 0)

        self.__boardWidget.setLayout(self.__boardWidgetLayout)
        self.__brd.setObjectName("brd")

        self.__editorWidget = PhtmEditorWidget(self.fileHandler , self)

        self.__splitter1 = QSplitter(Qt.Horizontal)
        self.__splitter1.addWidget(self.__boardWidget)
        self.__splitter1.addWidget(self.__editorWidget)
        self.__splitter1.setHandleWidth(1)
        self.__splitter1.setSizes([300, 325])

        self.body.setCentralWidget(self.__splitter1)
        
        self.body.statusBar().showMessage('Ready')
        self.body.statusBar().setFixedHeight(20)

        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)

        self.body.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setFixedWidth(200)

        self.MainToolBar = MainToolBar(self.fileHandler , self)
        self.MainToolBar.setUpToolBar()

        self.menuBar = PhtmMenuBar(self.fileHandler , self)
        self.menuBar.initMenuBar()
        self.fileHandler.setAdjustSignal(self.menuBar.getAdjustSignal())

        self.body.setMenuWidget(self.menuBar)

        self.show()

    def setWindowTitle(self, text):
        self.titleBar.setWindowTitle(text)
        self.setWindowTitle(text)

    def getWindowTitle(self):
        return self.getWindowTitle()

    def updateWindowTitle(self, newTitle):
        self.setWindowTitle(newTitle + " - " + self.getPermanentTitle())

    def getMainToolbar(self):
        return self.MainToolBar

    def getMenubar(self):
        return self.menuBar

    def getPermanentTitle(self):
        return self.__programTitle

    @pyqtSlot(str)
    def appendToBoard(self, message):
        # settings.__LOG__.logInfo(message)
        self.__brd.appendHtml(message)
        QCoreApplication.processEvents()

    def closeEvent(self, event):
        if self.changed:
            quitMessage = "Your changes have not been saved.\nAre you sure you want to exit the program?"
            reply = QMessageBox.question(self, 'Message', quitMessage, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            settings.__LOG__.logInfo("Program Ended")

    def showPref(self, index=0):
        preferenceDialog = PreferenceBody(self.getEditorWidget().getCluster(), self.user)
        preferenceDialog.tabW.setCurrentIndex(index)

        if preferenceDialog.exec_():
            self.reloadCurrDmi()
            self.reloadDbNames()

    def reloadDbNames(self):
        self.MainToolBar.dbnameMenu.currentTextChanged.disconnect()
        self.MainToolBar.dbnameMenu.clear()

        self.MainToolBar.dbnameMenu.addItems(DatabaseHandler.getDatabaseList(settings.__DATABASE__.getHostName(), settings.__DATABASE__.getPortNumber()))
        self.MainToolBar.dbnameMenu.currentTextChanged.connect(self.MainToolBar.databaseNameChanged)

        index = self.MainToolBar.dbnameMenu.findText(settings.__DATABASE__.getDatabaseName())
        self.MainToolBar.dbnameMenu.setCurrentIndex(index)

    def reloadCurrDmi(self):
        self.MainToolBar.currDmi.setPlainText(self.getEditorWidget().getCluster().getPhmScripts()["__dmi_instr__"]["name"])

    def getEditorWidget(self):
        return self.__editorWidget

    def newEditorWidget(self):
        if self.fileHandler.savePhm(self.menuBar.getAdjustSignal()):
            editorWidget = PhtmEditorWidget(self)
            self.setWindowTitle(self.__programTitle)
            self.__splitter1.replaceWidget(self.__splitter1.indexOf(self.__editorWidget), editorWidget)
            self.__editorWidget = editorWidget
            self.MainToolBar.dbnameMenu.setCurrentIndex(0)
