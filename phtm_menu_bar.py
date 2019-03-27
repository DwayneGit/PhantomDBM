import sys

from PyQt5.QtWidgets import QAction, QMenuBar

import file_ctrl as f_ctrl

class phtm_menu_bar(QMenuBar):
    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window

        self.main_menu = self
        self.recentFilesList = None

    def init_menu_bar(self):
        self.fileMenu()
        self.editMenu()
        self.helpMenu()

    def fileMenu(self):
        fileMenu = self.main_menu.addMenu('File')

        openJsonAction = QAction("Open JSON", self.mw)
        openJsonAction.setShortcut("Ctrl+O")
        openJsonAction.setStatusTip('Open a Script File')
        openJsonAction.triggered.connect(lambda: f_ctrl.getfile(self.mw, self.mw.get_editor_widget().get_editor_tabs().currentWidget()))
        fileMenu.addAction(openJsonAction)

        openPhmAction = QAction("Open PHM", self.mw)
        openPhmAction.setShortcut("Ctrl+P")
        openPhmAction.setStatusTip('Load a Cluster File')
        openPhmAction.triggered.connect(lambda: f_ctrl.load_phm(self.mw))
        fileMenu.addAction(openPhmAction)

        openRMenu = fileMenu.addMenu("Open Recent")
        # openRMenu.setLayoutDirection(Qt.LeftToRight)
        # openRMenu.setStatusTip('Open a Recent Script File')

        # for files in self.mw.getRecentFiles():
        #     #create fuction that creates an action to reopen recent file
        
        rfileAction = QAction("/path/to/recent/file", self.mw)
        openRMenu.addAction(rfileAction)
        # openRAction.triggered.connect(self.mw.getfile)
        fileMenu.addSeparator()

        savePAction = QAction("Save PHM", self.mw)
        savePAction.setShortcut("Ctrl+S")
        savePAction.setStatusTip('Save Script File')
        savePAction.triggered.connect(lambda: f_ctrl.saveScript(self.mw, self.mw.get_editor_widget().get_editor_tabs().currentWidget()))
        fileMenu.addAction(savePAction)

        savePAsAction = QAction("Save PHM As...", self.mw)
        savePAsAction.setShortcut("Ctrl+S")
        savePAsAction.setStatusTip('Save Script File')
        savePAsAction.triggered.connect(lambda: f_ctrl.saveScript(self.mw, self.mw.get_editor_widget().get_editor_tabs().currentWidget()))
        fileMenu.addAction(savePAsAction)
        fileMenu.addSeparator()

        importAction = QAction("Import JSON File", self.mw)
        importAction.setShortcut("Ctrl+S")
        importAction.setStatusTip('Save Script File')
        # importAction.triggered.connect(lambda: f_ctrl.saveScript(self.mw, self.mw.get_editor_widget().get_editor_tabs().currentWidget()))
        fileMenu.addAction(importAction)

        exportAction = QAction("Export JSON File", self.mw)
        exportAction.setShortcut("Ctrl+S")
        exportAction.setStatusTip('Save Script File')
        # exportAction.triggered.connect(lambda: f_ctrl.saveScript(self.mw, self.mw.get_editor_widget().get_editor_tabs().currentWidget()))
        fileMenu.addAction(exportAction)

        exittAction = QAction("Exit", self.mw)
        exittAction.setShortcut("Ctrl+Q")
        exittAction.setStatusTip('Leave The App')
        exittAction.triggered.connect(sys.exit)

        fileMenu.addSeparator()

        fileMenu.addAction(exittAction)

    def editMenu(self):
        undoAction = QAction("Undo", self.mw)
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(self.mw.get_editor_widget().get_editor_tabs().currentWidget().undo)

        redoAction = QAction("Redo", self.mw)
        redoAction.setShortcut("Ctrl+Y")
        redoAction.triggered.connect(self.mw.get_editor_widget().get_editor_tabs().currentWidget().redo)

        cutAction = QAction("Cut", self.mw)
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.mw.get_editor_widget().get_editor_tabs().currentWidget().cut)

        copyAction = QAction("Copy", self.mw)
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.mw.get_editor_widget().get_editor_tabs().currentWidget().copy)

        pasteAction = QAction("Paste", self.mw)
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.mw.get_editor_widget().get_editor_tabs().currentWidget().paste)

        findAction = QAction("FInd", self.mw)
        findAction.setShortcut("Ctrl+F")
        # findAction.triggered.connect()

        replaceAction = QAction("Replace", self.mw)
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

    def helpMenu(self):

        docAction = QAction("Documentation", self.mw)
        # docAction.triggered.connect(self.mw.fileContents.paste)

        notesAction = QAction("Release Notes", self.mw)
        # notesAction.triggered.connect(self.mw.fileContents.paste)

        updateAction = QAction("Check For Updates...", self.mw)
        # pasteAction.triggered.connect(self.mw.fileContents.paste)

        aboutAction = QAction("About", self.mw)
        # aboutAction.triggered.connect(self.mw.fileContents.paste)

        helpMenu = self.main_menu.addMenu('Help')
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
    