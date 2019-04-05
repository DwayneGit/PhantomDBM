"""-*- coding: utf-8 -*- """

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QToolBar, QAction, QWidget, QSizePolicy, QComboBox, QCheckBox

from database.DBConnection import database_handler

from phtm_widgets.phtm_tool_bar import phtm_tool_bar
from phtm_widgets.phtm_combo_box import phtm_combo_box
from phtm_widgets.phtm_plain_text_edit import phtm_plain_text_edit

import run_ctrl as r_ctrl
import file_ctrl as f_ctrl
from instructions.dmi_handler import dmi_handler

class main_tool_bar():
    """ application toolbars class """
    def __init__(self, main_window, icon_set):
        self.mw = main_window
        self.icon_set=icon_set

        self.instr_filepath = None
        self.instr_filename = None
    
    def setUpToolBar(self):

        #------------------ Top Toolbar ----------------------------
        topTBar = phtm_tool_bar()
        
        tbfile = QAction(QIcon(self.icon_set.import_file),"import",self.mw)
        tbfile.triggered.connect(lambda: f_ctrl.load_script(self.mw))
        topTBar.addAction(tbfile)
        
        tbsave = QAction(QIcon(self.icon_set.save),"save",self.mw)
        tbsave.triggered.connect(lambda: f_ctrl.save_script(self.mw, self.mw.get_editor_widget().get_editor_tabs().currentWidget()))
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

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # toolBar is a pointer to an existing toolbar
        topTBar.addWidget(spacer)

        # self.select_dmi = QAction(QIcon(self.icon_set.load_file),"import pre-uplaod instructions", self.mw)
        # self.select_dmi.triggered.connect(lambda: self.set_instructions())
        # topTBar.addAction(self.select_dmi)
        
        # self.dmi_selected = QCheckBox()
        # self.dmi_selected.setDisabled(True)
        # topTBar.addWidget(self.dmi_selected)
        
        self.curr_dmi = phtm_plain_text_edit(self.mw.prefs.prefDict["dmi"]["filename"])
        self.curr_dmi.setFixedSize(QSize(175,31))
        self.curr_dmi.setReadOnly(True)
        self.curr_dmi.mouseDoubleClickEvent = self.__open_dmi_prefs
        # self.currDMI.setFixedSize()
        topTBar.addWidget(self.curr_dmi)

        # ----------------- Side Toolbar ---------------------------
        sideTBar = phtm_tool_bar()
        tbload = QAction(QIcon(self.icon_set.load_file), "load", self.mw)
        # tbload.triggered.connect()
        sideTBar.addAction(tbload)
        
        tbedit = QAction(QIcon(self.icon_set.edit), "edit", self.mw)
        # tbedit.triggered.connect()
        sideTBar.addAction(tbedit)
        
        tbsettings = QAction(QIcon(self.icon_set.settings), "settings", self.mw)
        tbsettings.triggered.connect(self.mw.showPref)
        sideTBar.addAction(tbsettings)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # toolBar is a pointer to an existing toolbar
        sideTBar.addWidget(spacer)
        
        tbopen = QAction(QIcon(self.icon_set.wifi), "open", self.mw)
        # tbopen.triggered.connect()
        sideTBar.addAction(tbopen)
        
        dropdownSize = QSize(175,31)
        # self.mw.addrDropdownMenu = QComboBox()
        # self.mw.addrDropdownMenu.setFixedSize(dropdownSize)

        # sideTBar.addWidget(self.mw.addrDropdownMenu)
        
        self.dbnameMenu = phtm_combo_box()
        self.dbnameMenu.setFixedSize(dropdownSize)
        self.dbnameMenu.addItems(database_handler.getDatabaseList(self.mw.dbData['host'], self.mw.dbData['port']))

        index = self.dbnameMenu.findText(self.mw.prefs.prefDict['mongodb']['dbname'])
        self.dbnameMenu.setCurrentIndex(index)
        self.dbnameMenu.currentTextChanged.connect(lambda: databaseNameChanged(self, self.mw))

        sideTBar.addWidget(self.dbnameMenu)
        
        self.collnameMenu = phtm_combo_box()
        self.collnameMenu.setFixedSize(dropdownSize)
        self.collnameMenu.addItems(database_handler.getCollectionList(self.mw.dbData['host'], self.mw.dbData['port'], self.mw.dbData['dbname']))
        
        index = self.collnameMenu.findText(self.mw.prefs.prefDict['mongodb']['collection'])
        self.collnameMenu.setCurrentIndex(index)
        self.collnameMenu.currentTextChanged.connect(lambda: collectionNameChanged(self, self.mw))
        sideTBar.addWidget(self.collnameMenu)

        self.mw.addToolBar(Qt.TopToolBarArea, topTBar)
        self.mw.addToolBarBreak(Qt.TopToolBarArea)
        self.mw.addToolBar(Qt.TopToolBarArea, sideTBar)

    def set_instructions(self):
        self.instr_filename, self.instr_filepath = f_ctrl.load_instructions()
        # print(self.instr_filepath)
        # self.dmi_selected.setDisabled(False)
        self.curr_dmi.setPlainText(self.instr_filename)

    def get_instr_filepath(self):
        return self.instr_filepath

    def __open_dmi_prefs(self, e):
        print("clicked")

def collectionNameChanged(ptoolbar, main_window):
    main_window.dbData['collection'] = ptoolbar.collnameMenu.currentText()

def databaseNameChanged(ptoolbar, main_window):
    reloadCollectionNames(ptoolbar, main_window)
    main_window.dbData['dbname'] = ptoolbar.dbnameMenu.currentText()

def reloadCollectionNames(ptoolbar, main_window):
    ptoolbar.collnameMenu.currentTextChanged.disconnect()
    ptoolbar.collnameMenu.clear()
    # print(main_window.dbData)
    ptoolbar.collnameMenu.addItems(database_handler.getCollectionList(main_window.dbData['host'], main_window.dbData['port'], ptoolbar.dbnameMenu.currentText()))
    ptoolbar.collnameMenu.currentTextChanged.connect(lambda: collectionNameChanged(ptoolbar, main_window))

    index = ptoolbar.collnameMenu.findText(main_window.prefs.prefDict['mongodb']['collection'])
    ptoolbar.collnameMenu.setCurrentIndex(index)
    # print(main_window.prefs.prefDict)
    print(ptoolbar.collnameMenu.currentIndex())
    print(ptoolbar.collnameMenu.currentText())