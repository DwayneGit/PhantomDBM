import sys
import json

from PyQt5.QtWidgets import QAction, QMenuBar
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, pyqtSlot, QFileInfo
from PyQt5.QtGui import QDesktopServices

from Phantom.PhtmWidgets import PhtmMessageBox

from Phantom.Utility import validateJsonScript


from Phantom.ApplicationSettings import Settings

class PhtmMenuBar(QMenuBar):

    adjust = pyqtSignal(str)

    def __init__(self, fileHandler , parent):
        super().__init__()

        self.newPhmSignal = parent.newPhmSignal
        self.__editorWidget = parent.getEditorWidget()
        self.__r_ctrl = parent.getRunCtrl()

        self.adjust.connect(lambda x: self.adjustForCurrentFile(x))
        self.setContextMenuPolicy(Qt.PreventContextMenu)

        self.fileHandler = fileHandler 

        self.maxFileNum = 5
        self.recentFileActionList = []
        self.createActionsAndConnections()

    def initMenuBar(self):
        self.fileMenu()
        self.editMenu()
        self.runMenu()
        self.searchMenu()
        self.helpMenu()

    def getAdjustSignal(self):
        return self.adjust

    def searchMenu(self):
        searchMenu = self.addMenu('Search')

    def fileMenu(self):
        fileMenu = self.addMenu('File')

        newJsonAction = QAction("New Script", self)
        newJsonAction.setShortcut("Ctrl+N")
        newJsonAction.triggered.connect(self.__editorWidget.addNewScript)

        newPhmAction = QAction("New PHM", self)
        newPhmAction.setShortcut("Ctrl+N+P")
        newPhmAction.triggered.connect(self.newPhmSignal.emit)

        openJsonAction = QAction("Open Script", self)
        openJsonAction.setShortcut("Ctrl+O")
        openJsonAction.setStatusTip('Open a Script File')
        openJsonAction.triggered.connect(self.__editorWidget.loadScript)

        openPhmAction = QAction("Open PHM", self)
        openPhmAction.setShortcut("Ctrl+P")
        openPhmAction.setStatusTip('Load a Cluster File')
        openPhmAction.triggered.connect(lambda: self.fileHandler.loadPhm())
        savePAction = QAction("Save PHM", self)
        savePAction.setShortcut("Ctrl+S")
        savePAction.setStatusTip('Save Cluster File')
        savePAction.triggered.connect(lambda: self.fileHandler.savePhm())

        savePAsAction = QAction("Save PHM As...", self)
        savePAsAction.setStatusTip('Save Script File')
        savePAsAction.triggered.connect(lambda: self.fileHandler.savePhmAs())

        importAction = QAction("Import Script", self)
        importAction.setStatusTip('Save Script File')
        importAction.triggered.connect(self.__editorWidget.loadScript)

        exportAction = QAction("Export Script", self)
        exportAction.setStatusTip('Save Script File')
        exportAction.triggered.connect(lambda: self.fileHandler.exportScript())

        exittAction = QAction("Exit", self)
        exittAction.setShortcut("Ctrl+Q")
        exittAction.setStatusTip('Leave The App')
        exittAction.triggered.connect(sys.exit)

        fileMenu.addAction(newJsonAction)
        fileMenu.addAction(newPhmAction)
        fileMenu.addSeparator()

        fileMenu.addAction(openJsonAction)
        fileMenu.addAction(openPhmAction)
        openRecentMenu = fileMenu.addMenu("Open Recent")
        for rfile in self.recentFileActionList:
            openRecentMenu.addAction(rfile)
        self.updateRecentActionList()
        fileMenu.addSeparator()

        fileMenu.addAction(savePAction)
        fileMenu.addAction(savePAsAction)
        fileMenu.addSeparator()

        fileMenu.addAction(importAction)
        fileMenu.addAction(exportAction)
        fileMenu.addSeparator()

        fileMenu.addAction(exittAction)

    def editOperations(self, op):
        curr_wid = self.__editorWidget.getEditorTabs().currentWidget()
        if not curr_wid:
            return
        if op == 0:
            curr_wid.undo()
        if op == 1:
            curr_wid.redo()
        if op == 2:
            curr_wid.cut()
        if op == 3:
            curr_wid.copy()
        if op == 4:
            curr_wid.paste()

    def editMenu(self):
        editMenu = self.addMenu('Edit')

        undoAction = QAction("Undo", self)
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(lambda: self.editOperations(0))

        redoAction = QAction("Redo", self)
        redoAction.setShortcut("Ctrl+Y")
        redoAction.triggered.connect(lambda: self.editOperations(1))

        cutAction = QAction("Cut", self)
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(lambda: self.editOperations(2))

        copyAction = QAction("Copy", self)
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(lambda: self.editOperations(3))

        pasteAction = QAction("Paste", self)
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(lambda: self.editOperations(4))

        findAction = QAction("Find", self)
        findAction.setShortcut("Ctrl+F")
        # findAction.triggered.connect()

        replaceAction = QAction("Replace", self)
        replaceAction.setShortcut("Ctrl+H")
        # replaceAction.triggered.connect()

        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)
        editMenu.addSeparator()

        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)
        editMenu.addSeparator()

        editMenu.addAction(findAction)
        editMenu.addAction(replaceAction)

    def runMenu(self):
        runMenu = self.addMenu("Run")

        runAction = QAction("Run", self)
        runAction.setShortcut("Ctrl+R")
        runAction.triggered.connect(lambda: self.__r_ctrl.run(0)) 

        runAllAction = QAction("Run All", self)
        runAllAction.triggered.connect(lambda: self.__r_ctrl.run(1))

        stopAction = QAction("Stop", self)
        pauseAction = QAction("Pause", self)

        validateAction = QAction("Validate", self)
        validateAction.setShortcut("Ctrl+D")
        validateAction.triggered.connect(self.validateScript)

        runMenu.addAction(runAction)
        runMenu.addAction(runAllAction)
        runMenu.addAction(stopAction)
        runMenu.addAction(pauseAction)

        runMenu.addSeparator()
        runMenu.addAction(validateAction)

    def validateScript(self):
        try:
            validateJsonScript(self, self.__editorWidget.getEditorTabs().currentWidget().toPlainText())
        except Exception as err:
            errorMessage = PhtmMessageBox(self, "Invalid Json Error",
                            "Invalid Json Format\n" + str(err))
            errorMessage.exec_()
    
    def helpMenu(self):
        helpMenu = self.addMenu('Help')

        docAction = QAction("Documentation", self)
        docAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM/wiki")))

        notesAction = QAction("Release Notes", self)
        notesAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM/releases")))

        updateAction = QAction("Check For Updates...", self)
        updateAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM")))

        aboutAction = QAction("About", self)
        aboutAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM")))

        helpMenu.addAction(docAction)
        helpMenu.addAction(notesAction)
        helpMenu.addSeparator()

        helpMenu.addAction(updateAction)
        helpMenu.addSeparator()

        helpMenu.addAction(aboutAction)

    @pyqtSlot()
    def adjustForCurrentFile(self, filePath):

        recentFilePaths = Settings.__APPLICATION_SETTINGS__.getSettings()['recent_files']

        try:
            recentFilePaths.remove(filePath)
        except Exception as err:
            Settings.__LOG__.logError(str(err)+ str(type(err)))

        recentFilePaths.insert(0, filePath)

        while len(recentFilePaths) > self.maxFileNum:
            recentFilePaths.pop()

        self.updateRecentActionList()

    def updateRecentActionList(self):

        recentFilePaths = Settings.__APPLICATION_SETTINGS__.getSettings()['recent_files']

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

        Settings.__APPLICATION_SETTINGS__.updateSettings()

    def createActionsAndConnections(self):
        recentFileAction = None
        for i in range(0, self.maxFileNum):
            recentFileAction = QAction(self)
            recentFileAction.setVisible(False)
            recentFileAction.triggered.connect(self.openRecent)

            self.recentFileActionList.append(recentFileAction)

    def openRecent(self):
        if not self.fileHandler.loadPhm(self.sender().data()):
            recentFilePaths = Settings.__APPLICATION_SETTINGS__.getSettings()['recent_files']

            try:
                recentFilePaths.remove(self.sender().data())
            except Exception as err:
                Settings.__LOG__.logError("IOError: " + str(err))

            self.updateRecentActionList()