"""-*- coding: utf-8 -*- """

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QToolBar, QAction, QWidget, QSizePolicy, QComboBox

from DBConnection import DatabaseHandler

from style.phtm_tool_bar import phtm_tool_bar
from style.phtm_combo_box import phtm_combo_box

import run_ctrl as r_ctrl
import file_ctrl as f_ctrl

class main_tool_bar():
    """ application toolbars class """
    def __init__(self, main_window, icon_set):
        self.mw = main_window
        self.icon_set=icon_set
    
    def setUpToolBar(self):

        #------------------ Top Toolbar ----------------------------
        topTBar = phtm_tool_bar()
        
        tbfile = QAction(QIcon(self.icon_set.import_file),"import",self.mw)
        tbfile.triggered.connect(lambda: f_ctrl.load_script(self.mw))
        topTBar.addAction(tbfile)
        
        tbsave = QAction(QIcon(self.icon_set.save),"save",self.mw)
        tbsave.triggered.connect(lambda: f_ctrl.save_script(self.mw))
        topTBar.addAction(tbsave)
            
        tbfiles = QAction(QIcon(self.icon_set.export_file),"export",self.mw)
        tbfiles.triggered.connect(lambda: f_ctrl.export_script(self.mw))
        topTBar.addAction(tbfiles)
        
        self.tbrun = QAction()
        self.mw.setRunBtnAction(False)
        topTBar.addAction(self.tbrun)

        tbstop = QAction(QIcon(self.icon_set.stop),"stop",self.mw)
        tbstop.triggered.connect(lambda: r_ctrl.stopRun(self.mw))
        topTBar.addAction(tbstop)

        # ----------------- Side Toolbar ---------------------------
        sideTBar = phtm_tool_bar()
        tbload = QAction(QIcon(self.icon_set.load_file),"open",self.mw)
        # tbload.triggered.connect()
        sideTBar.addAction(tbload)
        
        tbedit = QAction(QIcon(self.icon_set.edit),"open",self.mw)
        # tbedit.triggered.connect()
        sideTBar.addAction(tbedit)
        
        tbsettings = QAction(QIcon(self.icon_set.settings),"open",self.mw)
        tbsettings.triggered.connect(self.mw.showPref)
        sideTBar.addAction(tbsettings)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # toolBar is a pointer to an existing toolbar
        sideTBar.addWidget(spacer)
        
        tbopen = QAction(QIcon(self.icon_set.wifi),"open",self.mw)
        # tbopen.triggered.connect()
        sideTBar.addAction(tbopen)
        
        dropdownSize = QSize(175,31)
        # self.mw.addrDropdownMenu = QComboBox()
        # self.mw.addrDropdownMenu.setFixedSize(dropdownSize)

        # sideTBar.addWidget(self.mw.addrDropdownMenu)
        
        self.dbnameMenu = phtm_combo_box()
        self.dbnameMenu.setFixedSize(dropdownSize)
        self.dbnameMenu.addItems(DatabaseHandler.getDatabaseList(self.mw.dbData['host'], self.mw.dbData['port']))

        index = self.dbnameMenu.findText(self.mw.prefs.prefDict['mongodb']['dbname'])
        self.dbnameMenu.setCurrentIndex(index)
        self.dbnameMenu.currentTextChanged.connect(lambda: databaseNameChanged(self, self.mw))

        sideTBar.addWidget(self.dbnameMenu)
        
        self.collnameMenu = phtm_combo_box()
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