import sys

from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Menubar():
    def __init__(self, mainWidget):
        self.mainWidget = mainWidget

        self.mainMenu = self.mainWidget.menuBar()
        self.recentFilesList = None


    def initMenubar(self):
        self.fileMenu()
        self.editMenu()
        self.helpMenu()

    def fileMenu(self):
        fileMenu = self.mainMenu.addMenu('File')

        openAction = QAction("Open File", self.mainWidget)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip('Open a Script File')
        openAction.triggered.connect(self.mainWidget.getfile)
        fileMenu.addAction(openAction)
        
        openRMenu = fileMenu.addMenu("Open Recent")
        # openRMenu.setLayoutDirection(Qt.LeftToRight)
        # openRMenu.setStatusTip('Open a Recent Script File')

        # for files in self.mainWidget.getRecentFiles():
        #     #create fuction that creates an action to reopen recent file
        
        rfileAction = QAction("/path/to/recent/file", self.mainWidget)
        openRMenu.addAction(rfileAction)
        # openRAction.triggered.connect(self.mainWidget.getfile)
        fileMenu.addSeparator()

        saveAction = QAction("Save File", self.mainWidget)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip('Save Script File')
        saveAction.triggered.connect(self.mainWidget.saveScript)

        exittAction = QAction("Exit", self.mainWidget)
        exittAction.setShortcut("Ctrl+Q")
        exittAction.setStatusTip('Leave The App')
        exittAction.triggered.connect(sys.exit)

        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()

        fileMenu.addAction(exittAction)

    def editMenu(self):
        undoAction = QAction("Undo", self.mainWidget)
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(self.mainWidget.fileContents.undo)

        redoAction = QAction("Redo", self.mainWidget)
        redoAction.setShortcut("Ctrl+Y")
        redoAction.triggered.connect(self.mainWidget.fileContents.redo)

        cutAction = QAction("Cut", self.mainWidget)
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.mainWidget.fileContents.cut)

        copyAction = QAction("Copy", self.mainWidget)
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.mainWidget.fileContents.copy)

        pasteAction = QAction("Paste", self.mainWidget)
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.mainWidget.fileContents.paste)

        findAction = QAction("FInd", self.mainWidget)
        findAction.setShortcut("Ctrl+F")
        # findAction.triggered.connect()

        replaceAction = QAction("Replace", self.mainWidget)
        replaceAction.setShortcut("Ctrl+H")
        # replaceAction.triggered.connect()
        
        editMenu = self.mainMenu.addMenu('Edit')
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

        docAction = QAction("Documentation", self.mainWidget)
        # docAction.triggered.connect(self.mainWidget.fileContents.paste)

        notesAction = QAction("Release Notes", self.mainWidget)
        # notesAction.triggered.connect(self.mainWidget.fileContents.paste)

        updateAction = QAction("Check For Updates...", self.mainWidget)
        # pasteAction.triggered.connect(self.mainWidget.fileContents.paste)

        aboutAction = QAction("About", self.mainWidget)
        # aboutAction.triggered.connect(self.mainWidget.fileContents.paste)

        helpMenu = self.mainMenu.addMenu('Help')
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
    