import sys

from PyQt5.QtWidgets import QAction, QMenuBar
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

from phantom.utility import validate_json_script
from phantom.file_stuff import file_ctrl as f_ctrl

class phtm_menu_bar(QMenuBar):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.main_menu = self
        self.recentFilesList = None

        self.setContextMenuPolicy(Qt.PreventContextMenu)

    def init_menu_bar(self):
        self.fileMenu()
        self.editMenu()
        self.runMenu()
        self.searchMenu()
        self.helpMenu()

    def searchMenu(self):
        searchMenu = self.main_menu.addMenu('Search')

    def fileMenu(self):
        fileMenu = self.main_menu.addMenu('File')

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
        openPhmAction.triggered.connect(lambda: f_ctrl.load_phm(self.parent))
        fileMenu.addAction(openPhmAction)

        openRMenu = fileMenu.addMenu("Open Recent")
        # openRMenu.setLayoutDirection(Qt.LeftToRight)
        # openRMenu.setStatusTip('Open a Recent Script File')

        # for files in self.parent.getRecentFiles():
        #     #create fuction that creates an action to reopen recent file
        
        rfileAction = QAction("/path/to/recent/file", self.parent)
        openRMenu.addAction(rfileAction)
        # openRAction.triggered.connect(self.parent.getfile)
        fileMenu.addSeparator()

        saveAction = QAction("Save Script", self.parent)
        saveAction.setStatusTip('Save Script File')
        saveAction.triggered.connect(lambda: f_ctrl.save_script(self.parent.get_editor_widget().get_editor_tabs().currentWidget(), self.parent.get_editor_widget()))
        fileMenu.addAction(saveAction)

        savePAction = QAction("Save PHM", self.parent)
        savePAction.setShortcut("Ctrl+S")
        savePAction.setStatusTip('Save Cluster File')
        savePAction.triggered.connect(lambda: f_ctrl.save_phm(self.parent.get_editor_widget()))
        fileMenu.addAction(savePAction)

        savePAsAction = QAction("Save PHM As...", self.parent)
        savePAsAction.setStatusTip('Save Script File')
        savePAsAction.triggered.connect(lambda: f_ctrl.export_phm(self.parent))
        fileMenu.addAction(savePAsAction)
        fileMenu.addSeparator()

        importAction = QAction("Import Script", self.parent)
        importAction.setStatusTip('Save Script File')
        importAction.triggered.connect(self.parent.get_editor_widget().load_script)
        fileMenu.addAction(importAction)

        exportAction = QAction("Export Script", self.parent)
        exportAction.setStatusTip('Save Script File')
        exportAction.triggered.connect(lambda: f_ctrl.export_script(self.parent.get_editor_widget().get_editor_tabs().currentWidget()))
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
        
        editMenu = self.main_menu.addMenu('Edit')
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
        runMenu = self.main_menu.addMenu("Run")

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
            QMessageBox.warning(self, "Invalid Json Error",
                            "Invalid Json Format\n" + str(err))            
            print(str(err))
    
    def helpMenu(self):
        helpMenu = self.main_menu.addMenu('Help')

        docAction = QAction("Documentation", self.parent)
        docAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM")))

        notesAction = QAction("Release Notes", self.parent)
        notesAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM")))

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

    def loadRecentFiles(self):
        pass

    def appendRecentFile(self):
        pass

    def getRecentFilesList(self):
        return self.recentFilesList