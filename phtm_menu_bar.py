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

        openAction = QAction("Open File", self.mw)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip('Open a Script File')
        openAction.triggered.connect(lambda: f_ctrl.getfile(self.mw))
        fileMenu.addAction(openAction)
        
        openRMenu = fileMenu.addMenu("Open Recent")
        # openRMenu.setLayoutDirection(Qt.LeftToRight)
        # openRMenu.setStatusTip('Open a Recent Script File')

        # for files in self.mw.getRecentFiles():
        #     #create fuction that creates an action to reopen recent file
        
        rfileAction = QAction("/path/to/recent/file", self.mw)
        openRMenu.addAction(rfileAction)
        # openRAction.triggered.connect(self.mw.getfile)
        fileMenu.addSeparator()

        saveAction = QAction("Save File", self.mw)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip('Save Script File')
        saveAction.triggered.connect(lambda: f_ctrl.saveScript(self.mw))

        exittAction = QAction("Exit", self.mw)
        exittAction.setShortcut("Ctrl+Q")
        exittAction.setStatusTip('Leave The App')
        exittAction.triggered.connect(sys.exit)

        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()

        fileMenu.addAction(exittAction)

    def editMenu(self):
        undoAction = QAction("Undo", self.mw)
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(self.mw.fileContents.undo)

        redoAction = QAction("Redo", self.mw)
        redoAction.setShortcut("Ctrl+Y")
        redoAction.triggered.connect(self.mw.fileContents.redo)

        cutAction = QAction("Cut", self.mw)
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.mw.fileContents.cut)

        copyAction = QAction("Copy", self.mw)
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.mw.fileContents.copy)

        pasteAction = QAction("Paste", self.mw)
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.mw.fileContents.paste)

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
    