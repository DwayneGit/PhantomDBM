from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 


def initMenuBar(obj, win):

    if win == 1 :
        mainMenu = obj.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        editMenu = mainMenu.addMenu('&Edit')
        helpMenu = mainMenu.addMenu('&Help')
            
        """
        File Menu
        """
        importdbButton = QAction(QIcon('none.png'), 'Import Database', obj)
        importdbButton.setStatusTip('Import Database')
        #importdbButton.triggered.connect(obj.close)
        fileMenu.addAction(importdbButton)

        exportdbButton = QAction(QIcon('none.png'), 'Export Database', obj)
        importdbButton.setStatusTip('Export Database')
        #importdbButton.triggered.connect(obj.close)
        fileMenu.addAction(exportdbButton)
            
        exitButton = QAction(QIcon('none.png'), 'Exit', obj)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(obj.close)
        fileMenu.addAction(exitButton)

        """
        Edit Menu
        """
        prefButton = QAction('Preferences', obj)
        prefButton.setStatusTip('Exit application')
        prefButton.triggered.connect(obj.showPref)
        editMenu.addAction(prefButton)

        """
        Edit Menu
        """
        docButton = QAction(QIcon('none.png'), 'Documentation', obj)
        docButton.setStatusTip('Documentation')
        #importdbButton.triggered.connect(obj.close)
        helpMenu.addAction(docButton)

        releaseButton = QAction(QIcon('none.png'), 'Release Notes', obj)
        releaseButton.setStatusTip('Release Notes')
        #importdbButton.triggered.connect(obj.close)
        helpMenu.addAction(releaseButton)

        aboutButton = QAction(QIcon('none.png'), 'About', obj)
        aboutButton.setStatusTip('About')
        #importdbButton.triggered.connect(obj.close)
        helpMenu.addAction(aboutButton)
        
