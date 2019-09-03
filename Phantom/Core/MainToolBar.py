"""-*- coding: utf-8 -*- """

from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QSize, pyqtSlot, QUrl
from PyQt5.QtWidgets import QAction, QWidget, QSizePolicy

from Phantom.Database import DatabaseHandler

from Phantom.PhtmWidgets import PhtmToolBar, PhtmComboBox, PhtmPlainTextEdit, PhtmAction

from Phantom.ApplicationSettings import Settings

class MainToolBar(QWidget):
    """ application toolbars class """
    def __init__(self, fileHandler, parent):
        super().__init__()

        self.preferenceSignal = parent.preferenceSignal
        self.__r_ctrl = parent.getRunCtrl()
        self.__editorWidget = parent.getEditorWidget()
        self.reloadDatabaseNames = parent.reloadDbNames

        self.instrFilepath = None
        self.instrFilename = None

        self.fileHandler  = fileHandler 

        self.isRunning = False
        self.isPaused = True

        self.__setupToolBar()

    def __setupToolBar(self):
        # ----------------- Top Toolbar ---------------------------
        self.__topToolBar = PhtmToolBar()
        self.__topToolBar.setMovable(False)

        blank = PhtmAction(Settings.styleSignal.iconSignal, Settings.__ICONS__.getAppIcon, "", self)
        blank.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM")))
        self.__topToolBar.addAction(blank)

        self.tbrun = QAction()
        self.setRunBtnAction(False)
        self.__topToolBar.addAction(self.tbrun)

        Settings.styleSignal.iconSignal.connect(lambda: self.setRunBtnAction(self.isRunning))

        tbstop = PhtmAction(Settings.styleSignal.iconSignal, Settings.__ICONS__.getStop, "Stop Run", self)
        tbstop.triggered.connect(lambda: self.setIsRunning(self.__r_ctrl.stopRun(self.isRunning)))
        self.__topToolBar.addAction(tbstop)

        self.currDmi = PhtmPlainTextEdit(self.__editorWidget.getCluster().getPhmScripts()["__dmi_instr__"]["name"])
        self.currDmi.setObjectName("dmi_edit")
        self.currDmi.setFixedSize(QSize(175, 31))
        self.currDmi.setReadOnly(True)
        self.currDmi.mouseDoubleClickEvent = self.__openDmiPreferences
        self.__topToolBar.addWidget(self.currDmi)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # toolBar is a pointer to an existing toolbar
        self.__topToolBar.addWidget(spacer)

        tbreload = PhtmAction(Settings.styleSignal.iconSignal, Settings.__ICONS__.getSync, "Sync To Client", self)
        tbreload.triggered.connect(self.reloadDatabaseNames)
        self.__topToolBar.addAction(tbreload)

        dropdownSize = QSize(175, 31)

        self.dbnameMenu = PhtmComboBox()
        self.dbnameMenu.setFixedSize(dropdownSize)
        self.dbnameMenu.addItems(DatabaseHandler.getDatabaseList(Settings.__DATABASE__.getHostName(), Settings.__DATABASE__.getPortNumber()))

        index = self.dbnameMenu.findText(Settings.__DATABASE__.getDatabaseName())
        self.dbnameMenu.setCurrentIndex(index)
        self.dbnameMenu.currentTextChanged.connect(lambda: self.databaseNameChanged())

        self.__topToolBar.addWidget(self.dbnameMenu)

        self.collnameMenu = PhtmComboBox()
        self.collnameMenu.setFixedSize(dropdownSize)
        try:
            self.collnameMenu.addItems(DatabaseHandler.getCollectionList(Settings.__DATABASE__.getHostName(), Settings.__DATABASE__.getPortNumber(), Settings.__DATABASE__.getDatabaseName()))
        except:
            Settings.__LOG__.logError("No collections found in database")

        index = self.collnameMenu.findText(Settings.__DATABASE__.getCollectionName())
        self.collnameMenu.setCurrentIndex(index)
        self.collnameMenu.currentTextChanged.connect(lambda: self.collectionNameChanged())
        
        self.__topToolBar.addWidget(self.collnameMenu)

        #------------------ Side Toolbar ----------------------------
        self.__sideToolBar = PhtmToolBar()
        self.__sideToolBar.setMovable(False)

        tbadd = PhtmAction(Settings.styleSignal.iconSignal, Settings.__ICONS__.getAdd, "Add Script", self)
        tbadd.triggered.connect(self.__editorWidget.addNewScript)
        self.__sideToolBar.addAction(tbadd)

        tbsave = PhtmAction(Settings.styleSignal.iconSignal, Settings.__ICONS__.getSave, "Save", self)
        tbsave.triggered.connect(lambda: self.fileHandler.savePhm())
        self.__sideToolBar.addAction(tbsave)

        tbphm = PhtmAction(Settings.styleSignal.iconSignal, Settings.__ICONS__.getImportFile, "Open PHM", self)
        tbphm.triggered.connect(lambda:self.fileHandler.loadPhm())
        self.__sideToolBar.addAction(tbphm)

        tbfiles = PhtmAction(Settings.styleSignal.iconSignal, Settings.__ICONS__.getExport, "Export Script", self)
        tbfiles.triggered.connect(lambda: self.fileHandler.exportScript())
        self.__sideToolBar.addAction(tbfiles)

        tbsettings = PhtmAction(Settings.styleSignal.iconSignal, Settings.__ICONS__.getSettings, "Settings", self)
        tbsettings.triggered.connect(lambda: self.preferenceSignal.emit(0))
        self.__sideToolBar.addAction(tbsettings)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__sideToolBar.addWidget(spacer)

        tbinfo = PhtmAction(Settings.styleSignal.iconSignal, Settings.__ICONS__.getInfo, "Info", self)
        tbinfo.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM/wiki")))
        self.__sideToolBar.addAction(tbinfo)

    def getTopToolBar(self):
        return self.__topToolBar

    def getSideToolBar(self):
        return self.__sideToolBar

    def setInstructions(self):
        self.instrFilename, self.instrFilepath = self.fileHandler.loadInstructions()
        self.currDmi.setPlainText(self.instrFilename)

    def getInstrFilepath(self):
        return self.instrFilepath

    def __openDmiPreferences(self, e):
        self.preferenceSignal.emit(1)

    def setRunState(self, state):
        self.setIsRunning(state)
        self.setRunBtnAction(state)

    def setIsRunning(self, state):
        self.isRunning = state

    def setRunBtnIcon(self, icon):
        self.tbrun.setIcon(icon)

    @pyqtSlot()
    def setRunBtnAction(self, state):
        if not state:
            self.setRunBtnIcon(QIcon(Settings.__ICONS__.getPlay()))
            self.tbrun.setIconText("run")
            # if self.parent.runs > 0:
            #     self.tbrun.triggered.disconnect()
            self.tbrun.triggered.connect(self.__run)

        elif state:
            self.setRunBtnIcon(QIcon(Settings.__ICONS__.getPause()))
            self.tbrun.setIconText("pause")
            self.tbrun.triggered.disconnect()

    def __run(self): 
        if self.__editorWidget.getEditorTabs().currentWidget():
            self.__r_ctrl.run(0)

    def databaseNameChanged(self):
        self.reloadCollectionNames()
        Settings.__DATABASE__.setDatabaseName(self.dbnameMenu.currentText())

    def collectionNameChanged(self):
        Settings.__DATABASE__.setCollectionName(self.collnameMenu.currentText())

    def reloadCollectionNames(self):
        self.collnameMenu.currentTextChanged.disconnect()
        self.collnameMenu.clear()

        self.collnameMenu.addItems(DatabaseHandler.getCollectionList(Settings.__DATABASE__.getHostName(), Settings.__DATABASE__.getPortNumber(), self.dbnameMenu.currentText()))
        self.collnameMenu.currentTextChanged.connect(lambda: self.collectionNameChanged())

        index = self.collnameMenu.findText(Settings.__DATABASE__.getCollectionName())
        self.collnameMenu.setCurrentIndex(index)
