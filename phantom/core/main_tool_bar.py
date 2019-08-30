"""-*- coding: utf-8 -*- """

from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QSize, pyqtSlot, QUrl
from PyQt5.QtWidgets import QAction, QWidget, QSizePolicy

from phantom.database import DatabaseHandler

from phantom.phtmWidgets import PhtmToolBar, PhtmComboBox, PhtmPlainTextEdit, PhtmAction

from phantom.applicationSettings import settings

class MainToolBar():
    """ application toolbars class """
    def __init__(self, fileHandler , parent):
        self.parent = parent

        self.instrFilepath = None
        self.instrFilename = None

        self.fileHandler  = fileHandler 

        self.isRunning = False
        self.isPaused = True

    def setUpToolBar(self):
        #------------------ Top Toolbar ----------------------------
        topTBar = PhtmToolBar()
        topTBar.setMovable(False)

        tbadd = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getAdd, "Add Script", self.parent)
        tbadd.triggered.connect(self.parent.getEditorWidget().addNewScript)
        topTBar.addAction(tbadd)

        tbsave = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getSave, "Save", self.parent)
        tbsave.triggered.connect(lambda: self.fileHandler.savePhm())
        topTBar.addAction(tbsave)

        tbphm = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getImportFile, "Open PHM", self.parent)
        tbphm.triggered.connect(lambda:self.fileHandler.loadPhm())
        topTBar.addAction(tbphm)

        tbfiles = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getExport, "Export Script", self.parent)
        tbfiles.triggered.connect(lambda: self.fileHandler.exportScript())
        topTBar.addAction(tbfiles)

        tbsettings = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getSettings, "Settings", self.parent)
        tbsettings.triggered.connect(self.parent.showPref)
        topTBar.addAction(tbsettings)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        topTBar.addWidget(spacer)

        tbinfo = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getInfo, "Info", self.parent)
        tbinfo.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM/wiki")))
        topTBar.addAction(tbinfo)

        # ----------------- Side Toolbar ---------------------------
        sideTBar = PhtmToolBar()
        sideTBar.setMovable(False)

        blank = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getAppIcon, "", self.parent)
        blank.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM")))
        sideTBar.addAction(blank)

        self.tbrun = QAction()
        self.setRunBtnAction(False)
        sideTBar.addAction(self.tbrun)

        settings.styleSignal.iconSignal.connect(lambda: self.setRunBtnAction(self.isRunning))

        tbstop = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getStop, "Stop Run", self.parent)
        tbstop.triggered.connect(lambda: self.setIsRunning(self.parent.r_ctrl.stopRun(self.isRunning)))
        sideTBar.addAction(tbstop)

        self.currDmi = PhtmPlainTextEdit(self.parent.getEditorWidget().getCluster().getPhmScripts()["__dmi_instr__"]["name"])
        self.currDmi.setObjectName("dmi_edit")
        self.currDmi.setFixedSize(QSize(175, 31))
        self.currDmi.setReadOnly(True)
        self.currDmi.mouseDoubleClickEvent = self.__openDmiPrefs
        sideTBar.addWidget(self.currDmi)

        # tbload = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getLoadFile), "load", self.parent)
        # # tbload.triggered.connect()
        # sideTBar.addAction(tbload)

        # tbedit = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getEdit), "edit", self.parent)
        # # tbedit.triggered.connect()
        # sideTBar.addAction(tbedit)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # toolBar is a pointer to an existing toolbar
        sideTBar.addWidget(spacer)

        tbreload = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getSync, "Sync To Client", self.parent)
        tbreload.triggered.connect(self.parent.reloadDbNames)
        sideTBar.addAction(tbreload)

        dropdownSize = QSize(175, 31)

        self.dbnameMenu = PhtmComboBox()
        self.dbnameMenu.setFixedSize(dropdownSize)
        self.dbnameMenu.addItems(DatabaseHandler.getDatabaseList(settings.__DATABASE__.getHostName(), settings.__DATABASE__.getPortNumber()))

        index = self.dbnameMenu.findText(settings.__DATABASE__.getDatabaseName())
        self.dbnameMenu.setCurrentIndex(index)
        self.dbnameMenu.currentTextChanged.connect(lambda: self.databaseNameChanged())

        sideTBar.addWidget(self.dbnameMenu)

        self.collnameMenu = PhtmComboBox()
        self.collnameMenu.setFixedSize(dropdownSize)
        try:
            self.collnameMenu.addItems(DatabaseHandler.getCollectionList(settings.__DATABASE__.getHostName(), settings.__DATABASE__.getPortNumber(), settings.__DATABASE__.getDatabaseName()))
        except:
            settings.__LOG__.logError("No collections found in database")

        index = self.collnameMenu.findText(settings.__DATABASE__.getCollectionName())
        self.collnameMenu.setCurrentIndex(index)
        self.collnameMenu.currentTextChanged.connect(lambda: self.collectionNameChanged())
        
        sideTBar.addWidget(self.collnameMenu)

        # tbalert = PhtmAction(settings.styleSignal.iconSignal, settings.__ICONS__.getWarning, "Schema Alert", self.parent)
        # tbalert.triggered.connect(lambda: print())
        # sideTBar.addAction(tbalert)

        self.parent.body.addToolBar(Qt.TopToolBarArea, sideTBar)
        self.parent.body.addToolBar(Qt.LeftToolBarArea, topTBar)

    def setInstructions(self):
        self.instrFilename, self.instrFilepath = self.fileHandler.loadInstructions()
        # self.dmi_selected.setDisabled(False)
        self.currDmi.setPlainText(self.instrFilename)

    def getInstrFilepath(self):
        return self.instrFilepath

    def __openDmiPrefs(self, e):
        self.parent.showPref(1)

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
            self.setRunBtnIcon(QIcon(settings.__ICONS__.getPlay()))
            self.tbrun.setIconText("run")
            # if self.parent.runs > 0:
            #     self.tbrun.triggered.disconnect()
            self.tbrun.triggered.connect(self.__run)

        elif state:
            self.setRunBtnIcon(QIcon(settings.__ICONS__.getPause()))
            self.tbrun.setIconText("pause")
            self.tbrun.triggered.disconnect()
    #         self.tbrun.triggered.connect(self.pauseRun)

    def __run(self): 
        if self.parent.getEditorWidget().getEditorTabs().currentWidget():
            self.parent.r_ctrl.run(0)

    def databaseNameChanged(self):
        self.reloadCollectionNames()
        settings.__DATABASE__.setDatabaseName(self.dbnameMenu.currentText())

    def collectionNameChanged(self):
        settings.__DATABASE__.setCollectionName(self.collnameMenu.currentText())

    def reloadCollectionNames(self):
        self.collnameMenu.currentTextChanged.disconnect()
        self.collnameMenu.clear()

        self.collnameMenu.addItems(DatabaseHandler.getCollectionList(settings.__DATABASE__.getHostName(), settings.__DATABASE__.getPortNumber(), self.dbnameMenu.currentText()))
        self.collnameMenu.currentTextChanged.connect(lambda: self.collectionNameChanged())

        index = self.collnameMenu.findText(settings.__DATABASE__.getCollectionName())
        self.collnameMenu.setCurrentIndex(index)
