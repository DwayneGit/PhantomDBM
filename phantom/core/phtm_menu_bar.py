import sys
import json

from PyQt5.QtWidgets import QAction, QMenuBar
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, pyqtSlot, QFileInfo
from PyQt5.QtGui import QDesktopServices

from phantom.phtm_widgets import PhtmMessageBox

from phantom.utility import validate_json_script


from phantom.application_settings import settings

class phtm_menu_bar(QMenuBar):

    adjust = pyqtSignal(str)

    def __init__(self, file_handler, parent):
        super().__init__()
        self.parent = parent
        self.adjust.connect(lambda x: self.adjustForCurrentFile(x))
        self.setContextMenuPolicy(Qt.PreventContextMenu)

        self.file_handler = file_handler

        self.maxFileNum = 4
        self.recentFileActionList = []
        self.createActionsAndConnections()

    def init_menu_bar(self):
        self.fileMenu()
        self.editMenu()
        self.runMenu()
        self.searchMenu()
        self.helpMenu()

    def get_adjust_signal(self):
        return self.adjust

    def searchMenu(self):
        searchMenu = self.addMenu('Search')

    def fileMenu(self):
        fileMenu = self.addMenu('File')

        newJsonAction = QAction("New Script", self.parent)
        newJsonAction.setShortcut("Ctrl+N")
        newJsonAction.triggered.connect(self.parent.get_editor_widget().add_new_script)
        fileMenu.addAction(newJsonAction)

        newPhmAction = QAction("New PHM", self.parent)
        newPhmAction.setShortcut("Ctrl+N+P")
        newPhmAction.triggered.connect(self.parent.new_editor_widget)
        fileMenu.addAction(newPhmAction)
        
        fileMenu.addSeparator()

        openJsonAction = QAction("Open Script", self.parent)
        openJsonAction.setShortcut("Ctrl+O")
        openJsonAction.setStatusTip('Open a Script File')
        openJsonAction.triggered.connect(self.parent.get_editor_widget().load_script)
        fileMenu.addAction(openJsonAction)

        openPhmAction = QAction("Open PHM", self.parent)
        openPhmAction.setShortcut("Ctrl+P")
        openPhmAction.setStatusTip('Load a Cluster File')
        openPhmAction.triggered.connect(lambda: self.file_handler.load_phm())
        fileMenu.addAction(openPhmAction)

        openRecentMenu = fileMenu.addMenu("Open Recent")
        for rfile in self.recentFileActionList:
            openRecentMenu.addAction(rfile)
        self.updateRecentActionList()
        fileMenu.addSeparator()
        savePAction = QAction("Save PHM", self.parent)
        savePAction.setShortcut("Ctrl+S")
        savePAction.setStatusTip('Save Cluster File')
        savePAction.triggered.connect(lambda: self.file_handler.save_phm())
        fileMenu.addAction(savePAction)

        savePAsAction = QAction("Save PHM As...", self.parent)
        savePAsAction.setStatusTip('Save Script File')
        savePAsAction.triggered.connect(lambda: self.file_handler.export_phm())
        fileMenu.addAction(savePAsAction)
        fileMenu.addSeparator()

        importAction = QAction("Import Script", self.parent)
        importAction.setStatusTip('Save Script File')
        importAction.triggered.connect(self.parent.get_editor_widget().load_script)
        fileMenu.addAction(importAction)

        exportAction = QAction("Export Script", self.parent)
        exportAction.setStatusTip('Save Script File')
        exportAction.triggered.connect(lambda: self.file_handler.export_script())
        fileMenu.addAction(exportAction)

        exittAction = QAction("Exit", self.parent)
        exittAction.setShortcut("Ctrl+Q")
        exittAction.setStatusTip('Leave The App')
        exittAction.triggered.connect(sys.exit)

        fileMenu.addSeparator()

        fileMenu.addAction(exittAction)

    def editMenu(self):
        undoAction = QAction("Undo", self.parent)
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(lambda: self.f_undo(0))

        redoAction = QAction("Redo", self.parent)
        redoAction.setShortcut("Ctrl+Y")
        redoAction.triggered.connect(lambda: self.f_undo(1))

        cutAction = QAction("Cut", self.parent)
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(lambda: self.f_undo(2))

        copyAction = QAction("Copy", self.parent)
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(lambda: self.f_undo(3))

        pasteAction = QAction("Paste", self.parent)
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(lambda: self.f_undo(4))

        findAction = QAction("Find", self.parent)
        findAction.setShortcut("Ctrl+F")
        # findAction.triggered.connect()

        replaceAction = QAction("Replace", self.parent)
        replaceAction.setShortcut("Ctrl+H")
        # replaceAction.triggered.connect()
        
        editMenu = self.addMenu('Edit')
        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)
        editMenu.addSeparator()

        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)
        editMenu.addSeparator()

        editMenu.addAction(findAction)
        editMenu.addAction(replaceAction)

    def edit_operations(self, op):
        curr_wid = self.parent.get_editor_widget().get_editor_tabs().currentWidget()
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

    def runMenu(self):
        runMenu = self.addMenu("Run")

        runAction = QAction("Run", self.parent)
        runAction.setShortcut("Ctrl+R")
        runAction.triggered.connect(lambda: self.parent.r_ctrl.run(0)) 

        runAllAction = QAction("Run All", self.parent)
        runAllAction.triggered.connect(lambda: self.parent.r_ctrl.run(1))

        stopAction = QAction("Stop", self.parent)
        pauseAction = QAction("Pause", self.parent)

        runMenu.addAction(runAction)
        runMenu.addAction(runAllAction)
        runMenu.addAction(stopAction)
        runMenu.addAction(pauseAction)

        runMenu.addSeparator()

        validateAction = QAction("Validate", self.parent)
        validateAction.setShortcut("Ctrl+D")
        validateAction.triggered.connect(self.validate_script)
        runMenu.addAction(validateAction)

    def validate_script(self):
        try:
            validate_json_script(self, self.parent.get_editor_widget().get_editor_tabs().currentWidget().toPlainText())
        except Exception as err:
            err_msg = PhtmMessageBox(self, "Invalid Json Error",
                            "Invalid Json Format\n" + str(err))
            err_msg.exec_()
    
    def helpMenu(self):
        helpMenu = self.addMenu('Help')

        docAction = QAction("Documentation", self.parent)
        docAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM/wiki")))

        notesAction = QAction("Release Notes", self.parent)
        notesAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM/releases")))

        updateAction = QAction("Check For Updates...", self.parent)
        updateAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM")))

        aboutAction = QAction("About", self.parent)
        aboutAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM")))

        helpMenu.addAction(docAction)
        helpMenu.addAction(notesAction)
        helpMenu.addSeparator()

        helpMenu.addAction(updateAction)
        helpMenu.addSeparator()

        helpMenu.addAction(aboutAction)

    @pyqtSlot()
    def adjustForCurrentFile(self, filePath):

        recentFilePaths = settings.__APPLICATION_SETTINGS__.get_settings()['recent_files']

        try:
            recentFilePaths.remove(filePath)
        except Exception as err:
            settings.__LOG__.logError(str(err)+ str(type(err)))

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
            recentFileAction = QAction(self)
            recentFileAction.setVisible(False)
            recentFileAction.triggered.connect(self.openRecent)

            self.recentFileActionList.append(recentFileAction)

    def openRecent(self):
        if not self.file_handler.load_phm(self.sender().data()):
            recentFilePaths = settings.__APPLICATION_SETTINGS__.get_settings()['recent_files']

            try:
                recentFilePaths.remove(self.sender().data())
            except Exception as err:
                settings.__LOG__.logError("IOError: " + str(err))

            self.updateRecentActionList()