from copy import deepcopy
import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect, Qt, QCoreApplication, pyqtSlot, QFileInfo, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QSplitter, QProgressBar, QMessageBox, QWidget, QHBoxLayout, QAction, QVBoxLayout

from Phantom.Users import loginScreen
from Phantom.Database import DatabaseHandler
from Phantom.Utility import centerWindow

from Phantom.Preferences import PreferenceBody
from Phantom.ApplicationSettings import Settings

from Phantom.PhtmWidgets import PhtmDialog, PhtmPlainTextEdit, PhtmTitleBar

from Phantom.file_stuff import FileHandler

from . import RunCtrl
from . import PhtmMenuBar
from . import MainToolBar
from . import PhtmEditorWidget

BUFFERSIZE = 1000

class MainWindow(QMainWindow):
    runs = 0
    completedRunCounter = 0

    statusBarSignal = pyqtSignal(str, int)
    progressSignal = pyqtSignal(int)
    progressMaxSignal = pyqtSignal(int)
    preferenceSignal = pyqtSignal(int)
    boardSignal = pyqtSignal(str)
    newPhmSignal = pyqtSignal()
    windowTitleSignal = pyqtSignal(str)
    reloadDatabaseSignal = pyqtSignal()
    reloadDmiSignal = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()

        Settings.__LOG__.logInfo("Program Started.")
        self.setObjectName("pmainwind")

        self.user = None
        self.changed = False
        self.windowTitle = ''
        self.__editorWidget = None

        self.__titleBar = PhtmTitleBar(self, True)
        self.__titleBar.generateTitleBar()

        self.__programTitle = "PhantomDBM"
        self.setMainWindowTitle(self.__programTitle)

        self.oldPos = self.pos()
        self.setWindowIcon(QIcon("icons/logo.png"))

        self.setGeometry(QRect(10, 10, 1100, 620)) # left, top, width, height
        self.move(centerWindow(self))

        self.layout().setSpacing(0)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.addToolBar(Qt.TopToolBarArea, self.__titleBar)

        self.__r_ctrl = RunCtrl(self)

        self.__body = QMainWindow()
        self.setCentralWidget(self.__body)

        self.fileHandler = FileHandler(self)
        login = PhtmDialog("Login", QRect(10, 10, 260, 160), self)
        login.setCentralDialog(loginScreen(login))

        self.__initUI()

        # if login.exec_():
        #     Settings.__LOG__.logInfo("Successfully Logged In.")
        #     self.user = login.getCentralDialog().user
        #     self.initUI()
        # else:
        #     Settings.__LOG__.logInfo("No login program exited.")
        #     sys.exit()

    def __initUI(self):

        self.__boardWidget = QWidget()
        self.__boardWidgetLayout = QHBoxLayout()

        self.__board = PhtmPlainTextEdit()
        self.__board.setReadOnly(True)
        self.__board.insertPlainText("Welcome to Phantom Database Manager (DBM).")

        self.__boardWidgetLayout.addWidget(self.__board)
        self.__boardWidgetLayout.setContentsMargins(0, 0, 0, 0)

        self.__boardWidget.setLayout(self.__boardWidgetLayout)
        self.__board.setObjectName("board")

        self.__editorWidget = PhtmEditorWidget(self.fileHandler, self)
        self.fileHandler.setEditorWidget(self.__editorWidget)

        self.__mainSplitter = QSplitter(Qt.Horizontal)
        self.__mainSplitter.addWidget(self.__boardWidget)
        self.__mainSplitter.addWidget(self.__editorWidget)
        self.__mainSplitter.setHandleWidth(1)
        self.__mainSplitter.setSizes([300, 325])

        self.__body.setCentralWidget(self.__mainSplitter)
        
        self.__body.statusBar().showMessage('Ready')
        self.__body.statusBar().setFixedHeight(20)

        self.__progressBar = QProgressBar()
        self.__progressBar.setTextVisible(False)
        self.__progressBar.setFixedWidth(200)
        self.progressSignal.connect(self.updateProgress)
        self.progressMaxSignal.connect(self.setProgressMax)

        self.__body.statusBar().addPermanentWidget(self.__progressBar)
        self.statusBarSignal.connect(self.updateStatusBar)

        self.__mainToolBar = MainToolBar(self.fileHandler , self)

        self.__body.addToolBar(Qt.TopToolBarArea, self.__mainToolBar.getTopToolBar())
        self.__body.addToolBar(Qt.LeftToolBarArea, self.__mainToolBar.getSideToolBar())

        self.__r_ctrl.setMainToolbar(self.__mainToolBar)

        self.__menuBar = PhtmMenuBar(self.fileHandler, self)
        self.__menuBar.initMenuBar()
        self.fileHandler.setAdjustSignal(self.__menuBar.getAdjustSignal())

        self.fileHandler.setMenuBar(self.__menuBar)
        self.__body.setMenuWidget(self.__menuBar)

        self.preferenceSignal.connect(self.showPreferences)
        self.boardSignal.connect(self.appendToBoard)
        self.newPhmSignal.connect(self.newEditorWidget)
        self.windowTitleSignal.connect(self.updateWindowTitle)
        self.reloadDatabaseSignal.connect(self.reloadDbNames)
        self.reloadDmiSignal.connect(self.reloadCurrDmi)

    def setMainWindowTitle(self, text):
        self.__titleBar.setWindowTitle(text)
        self.setWindowTitle(text)

    def getWindowTitle(self):
        return self.getWindowTitle()

    def getMainToolbar(self):
        return self.__mainToolBar

    def getMenubar(self):
        return self.__menuBar

    def getRunCtrl(self):
        return self.__r_ctrl

    def getPermanentTitle(self):
        return self.__programTitle
        self.show()

    @pyqtSlot(str)
    def updateWindowTitle(self, newTitle):
        self.setMainWindowTitle(newTitle + " - " + self.getPermanentTitle())

    @pyqtSlot(str)
    def appendToBoard(self, message):
        self.__board.appendHtml(message)
        QCoreApplication.processEvents()

    @pyqtSlot(str, int)
    def updateStatusBar(self, message, time):
        self.__body.statusBar().showMessage(message, time)

    @pyqtSlot(int)
    def setProgressMax(self, max):
        self.__progressBar.setMaximum(value)

    @pyqtSlot(int)
    def updateProgress(self, value):
        if value != -1:
            self.__progressBar.setValue(value)
        else:
            self.__progressBar.setValue(self.__progressBar.value()+1)

    @pyqtSlot(int)
    def showPreferences(self, index):
        preferenceDialog = PreferenceBody(self.getEditorWidget().getCluster(), self.user)
        preferenceDialog.tabW.setCurrentIndex(index)

        if preferenceDialog.exec_():
            self.reloadCurrDmi()
            self.reloadDbNames()

    @pyqtSlot()
    def newEditorWidget(self):
        if self.fileHandler.savePhm(self.__menuBar.getAdjustSignal()):
            editorWidget = PhtmEditorWidget(self)
            self.setMainWindowTitle(self.__programTitle)
            self.__mainSplitter.replaceWidget(self.__mainSplitter.indexOf(self.__editorWidget), editorWidget)
            self.__editorWidget = editorWidget
            self.__mainToolBar.dbnameMenu.setCurrentIndex(0)

    @pyqtSlot()
    def reloadDbNames(self):
        self.__mainToolBar.dbnameMenu.currentTextChanged.disconnect()
        self.__mainToolBar.dbnameMenu.clear()

        self.__mainToolBar.dbnameMenu.addItems(DatabaseHandler.getDatabaseList(Settings.__DATABASE__.getHostName(), Settings.__DATABASE__.getPortNumber()))
        self.__mainToolBar.dbnameMenu.currentTextChanged.connect(self.__mainToolBar.databaseNameChanged)

        index = self.__mainToolBar.dbnameMenu.findText(Settings.__DATABASE__.getDatabaseName())
        self.__mainToolBar.dbnameMenu.setCurrentIndex(index)

    @pyqtSlot()
    def reloadCurrDmi(self):
        self.__mainToolBar.currDmi.setPlainText(self.getEditorWidget().getCluster().getPhmScripts()["__dmi_instr__"]["name"])

    def getEditorWidget(self):
        return self.__editorWidget

    def closeEvent(self, event):
        print("I'm out Gee")
        if self.changed:
            quitMessage = "Your changes have not been saved.\nAre you sure you want to exit the program?"
            reply = QMessageBox.question(self, 'Message', quitMessage, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            Settings.__LOG__.logInfo("Program Ended")
