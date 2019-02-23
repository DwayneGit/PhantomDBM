"""-*- coding: utf-8 -*- """

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QToolBar, QAction, QWidget, QSizePolicy, QComboBox

from DBConnection import DatabaseHandler

import run_ctrl as r_ctrl
import file_ctrl as f_ctrl

class phtm_tool_bar():
    """ application toolbars class """
    def __init__(self, main_window):
        self.mw = main_window
    
    def setUpToolBar(self):

        #------------------ Top Toolbar ----------------------------
        topTBar = QToolBar(self.mw)
        
        tbfile = QAction(QIcon("icons/import-file.png"),"import",self.mw)
        tbfile.triggered.connect(lambda: f_ctrl.getfile(self.mw))
        topTBar.addAction(tbfile)
        
        tbsave = QAction(QIcon("icons/save.png"),"save",self.mw)
        tbsave.triggered.connect(lambda: f_ctrl.saveScript(self.mw))
        topTBar.addAction(tbsave)
            
        tbfiles = QAction(QIcon("icons/export-file.png"),"export",self.mw)
        tbfiles.triggered.connect(lambda: f_ctrl.exportScript(self.mw))
        topTBar.addAction(tbfiles)
        
        self.tbrun = QAction()
        self.mw.setRunBtnAction(False)
        topTBar.addAction(self.tbrun)

        tbstop = QAction(QIcon("icons/stop.png"),"stop",self.mw)
        tbstop.triggered.connect(lambda: r_ctrl.stopRun(self.mw))
        topTBar.addAction(tbstop)

        # ----------------- Side Toolbar ---------------------------
        sideTBar = QToolBar(self.mw)
        tbload = QAction(QIcon("icons/load-file.png"),"open",self.mw)
        # tbload.triggered.connect()
        sideTBar.addAction(tbload)
        
        tbedit = QAction(QIcon("icons/editor.png"),"open",self.mw)
        # tbedit.triggered.connect()
        sideTBar.addAction(tbedit)
        
        tbsettings = QAction(QIcon("icons/settings.png"),"open",self.mw)
        tbsettings.triggered.connect(self.mw.showPref)
        sideTBar.addAction(tbsettings)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # toolBar is a pointer to an existing toolbar
        sideTBar.addWidget(spacer)
        
        tbopen = QAction(QIcon("icons/internet.png"),"open",self.mw)
        # tbopen.triggered.connect()
        sideTBar.addAction(tbopen)
        
        dropdownSize = QSize(175,31)
        # self.mw.addrDropdownMenu = QComboBox()
        # self.mw.addrDropdownMenu.setFixedSize(dropdownSize)

        # sideTBar.addWidget(self.mw.addrDropdownMenu)
        
        self.dbnameMenu = QComboBox()
        self.dbnameMenu.setFixedSize(dropdownSize)
        self.dbnameMenu.addItems(DatabaseHandler.getDatabaseList(self.mw.dbData['host'], self.mw.dbData['port']))

        index = self.dbnameMenu.findText(self.mw.prefs.prefDict['mongodb']['dbname'])
        self.dbnameMenu.setCurrentIndex(index)
        self.dbnameMenu.currentTextChanged.connect(lambda: databaseNameChanged(self, self.mw))

        sideTBar.addWidget(self.dbnameMenu)
        
        self.collnameMenu = QComboBox()
        self.collnameMenu.setFixedSize(dropdownSize)
        self.collnameMenu.addItems(DatabaseHandler.getCollectionList(self.mw.dbData['host'], self.mw.dbData['port'], self.mw.dbData['dbname']))
        
        index = self.collnameMenu.findText(self.mw.prefs.prefDict['mongodb']['collection'])
        self.collnameMenu.setCurrentIndex(index)
        self.collnameMenu.currentTextChanged.connect(lambda: collectionNameChanged(self, self.mw))
        sideTBar.addWidget(self.collnameMenu)

        self.mw.addToolBar(Qt.TopToolBarArea, topTBar)
        self.mw.addToolBar(Qt.TopToolBarArea, sideTBar)

def collectionNameChanged(ptoolbar, main_window):
    main_window.dbData['collection'] = ptoolbar.collnameMenu.currentText()

def databaseNameChanged(ptoolbar, main_window):
    reloadCollectionNames(ptoolbar, main_window)
    main_window.dbData['dbname'] = ptoolbar.dbnameMenu.currentText()

def reloadCollectionNames(ptoolbar, main_window):
    ptoolbar.collnameMenu.clear()
    ptoolbar.collnameMenu.addItems(DatabaseHandler.getCollectionList(main_window.dbData['host'], main_window.dbData['port'], ptoolbar.dbnameMenu.currentText()))
    index = ptoolbar.collnameMenu.findText(main_window.prefs.prefDict['mongodb']['collection'])
    ptoolbar.collnameMenu.setCurrentIndex(index)