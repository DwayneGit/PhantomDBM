"""-*- coding: utf-8 -*- """

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QAction, QWidget, QSizePolicy

from phantom.database import database_handler

from phantom.phtm_widgets import PhtmToolBar
from phantom.phtm_widgets import PhtmComboBox
from phantom.phtm_widgets import PhtmPlainTextEdit

from phantom.file_stuff import file_ctrl as f_ctrl

from phantom.application_settings import settings

class main_tool_bar():
    """ application toolbars class """
    def __init__(self, parent):
        self.parent = parent

        self.instr_filepath = None
        self.instr_filename = None

        self.isRunning = False
        self.isPaused = True

    def setUpToolBar(self):
        #------------------ Top Toolbar ----------------------------
        topTBar = PhtmToolBar()
        topTBar.setMovable(False)

        tbadd = QAction(QIcon(settings.__ICONS__.add), "Add Script", self.parent)
        tbadd.triggered.connect(self.parent.get_editor_widget().add_new_script)
        topTBar.addAction(tbadd)

        tbsave = QAction(QIcon(settings.__ICONS__.save), "Save", self.parent)
        tbsave.triggered.connect(lambda: f_ctrl.save_script(self.parent.get_editor_widget().get_editor_tabs().currentWidget(), self.parent.get_editor_widget()))
        topTBar.addAction(tbsave)

        tbphm = QAction(QIcon(settings.__ICONS__.import_file), "Open PHM", self.parent)
        tbphm.triggered.connect(f_ctrl.load_phm)
        topTBar.addAction(tbphm)

        tbfiles = QAction(QIcon(settings.__ICONS__.export), "Export Script", self.parent)
        tbfiles.triggered.connect(lambda: f_ctrl.export_script(self.parent.get_editor_widget().get_editor_tabs().currentWidget().toPlainText()))
        topTBar.addAction(tbfiles)

        tbsettings = QAction(QIcon(settings.__ICONS__.settings), "sSettings", self.parent)
        tbsettings.triggered.connect(self.parent.showPref)
        topTBar.addAction(tbsettings)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        topTBar.addWidget(spacer)

        tbinfo = QAction(QIcon(settings.__ICONS__.info), "Info", self.parent)
        tbinfo.triggered.connect(lambda: self.parent.showPref())
        topTBar.addAction(tbinfo)

        # ----------------- Side Toolbar ---------------------------
        sideTBar = PhtmToolBar()
        sideTBar.setMovable(False)

        blank = QAction(QIcon(settings.__ICONS__.app_icon), "", self.parent)
        sideTBar.addAction(blank)

        self.tbrun = QAction()
        self.setRunBtnAction(False)
        sideTBar.addAction(self.tbrun)

        tbstop = QAction(QIcon(settings.__ICONS__.stop), "Stop Run", self.parent)
        tbstop.triggered.connect(lambda: self.setIsRunning(self.parent.r_ctrl.stopRun(self.isRunning)))
        sideTBar.addAction(tbstop)

        self.curr_dmi = PhtmPlainTextEdit(self.parent.get_editor_widget().get_cluster().get_phm_scripts()["__dmi_instr__"]["name"])
        self.curr_dmi.setObjectName("dmi_edit")
        self.curr_dmi.setFixedSize(QSize(175, 31))
        self.curr_dmi.setReadOnly(True)
        self.curr_dmi.mouseDoubleClickEvent = self.__open_dmi_prefs
        sideTBar.addWidget(self.curr_dmi)

        # tbload = QAction(QIcon(settings.__ICONS__.load_file), "load", self.parent)
        # # tbload.triggered.connect()
        # sideTBar.addAction(tbload)

        # tbedit = QAction(QIcon(settings.__ICONS__.edit), "edit", self.parent)
        # # tbedit.triggered.connect()
        # sideTBar.addAction(tbedit)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # toolBar is a pointer to an existing toolbar
        sideTBar.addWidget(spacer)

        tbreload = QAction(QIcon(settings.__ICONS__.sync), "Sync To Client", self.parent)
        tbreload.triggered.connect(self.parent.reloadDbNames)
        sideTBar.addAction(tbreload)

        dropdownSize = QSize(175, 31)

        self.dbnameMenu = PhtmComboBox()
        self.dbnameMenu.setFixedSize(dropdownSize)
        self.dbnameMenu.addItems(database_handler.getDatabaseList(self.parent.dbData['host'], self.parent.dbData['port']))

        index = self.dbnameMenu.findText(self.parent.prefs['mongodb']['dbname'])
        self.dbnameMenu.setCurrentIndex(index)
        self.dbnameMenu.currentTextChanged.connect(lambda: databaseNameChanged(self, self.parent))

        sideTBar.addWidget(self.dbnameMenu)

        self.collnameMenu = PhtmComboBox()
        self.collnameMenu.setFixedSize(dropdownSize)
        try:
            self.collnameMenu.addItems(database_handler.getCollectionList(self.parent.dbData['host'], self.parent.dbData['port'], self.parent.dbData['dbname']))
        except:
            settings.__LOG__.logError("No collections found in database")

        index = self.collnameMenu.findText(self.parent.prefs['mongodb']['collection'])
        self.collnameMenu.setCurrentIndex(index)
        self.collnameMenu.currentTextChanged.connect(lambda: collectionNameChanged(self, self.parent))
        sideTBar.addWidget(self.collnameMenu)

        self.parent.addToolBar(Qt.TopToolBarArea, sideTBar)
        self.parent.addToolBar(Qt.LeftToolBarArea, topTBar)

    def set_instructions(self):
        self.instr_filename, self.instr_filepath = f_ctrl.load_instructions()
        # self.dmi_selected.setDisabled(False)
        self.curr_dmi.setPlainText(self.instr_filename)

    def get_instr_filepath(self):
        return self.instr_filepath

    def __open_dmi_prefs(self, e):
        self.parent.showPref(1)

    def setRunState(self, state):
        self.setIsRunning(state)
        self.setRunBtnAction(state)

    def setIsRunning(self, state):
        self.isRunning = state

    def setRunBtnIcon(self, icon):
        self.tbrun.setIcon(icon)

    def setRunBtnAction(self, state):
        if not state:
            self.setRunBtnIcon(QIcon(settings.__ICONS__.play))
            self.tbrun.setIconText("run")
            # if self.parent.runs > 0:
            #     self.tbrun.triggered.disconnect()
            self.tbrun.triggered.connect(self.__run)

        elif state:
            self.setRunBtnIcon(QIcon(settings.__ICONS__.pause))
            self.tbrun.setIconText("pause")
            self.tbrun.triggered.disconnect()
    #         self.tbrun.triggered.connect(self.pauseRun)

    def __run(self): 
        if self.parent.get_editor_widget().get_editor_tabs().currentWidget():
            self.parent.r_ctrl.run(0)

def collectionNameChanged(ptoolbar, main_window, edit_widget=0, db_data=0):
    main_window.dbData['collection'] = ptoolbar.collnameMenu.currentText()
    main_window.get_editor_widget().get_cluster().save_settings(col=ptoolbar.collnameMenu.currentText())

def databaseNameChanged(ptoolbar, main_window, edit_widget=0, db_data=0):
    reloadCollectionNames(ptoolbar, main_window)
    main_window.dbData['dbname'] = ptoolbar.dbnameMenu.currentText()
    main_window.get_editor_widget().get_cluster().save_settings(db=ptoolbar.dbnameMenu.currentText())

def reloadCollectionNames(ptoolbar, main_window, edit_widget=0, db_data=0):
    ptoolbar.collnameMenu.currentTextChanged.disconnect()
    ptoolbar.collnameMenu.clear()

    ptoolbar.collnameMenu.addItems(database_handler.getCollectionList(main_window.dbData['host'], main_window.dbData['port'], ptoolbar.dbnameMenu.currentText()))
    ptoolbar.collnameMenu.currentTextChanged.connect(lambda: collectionNameChanged(ptoolbar, main_window))

    index = ptoolbar.collnameMenu.findText(main_window.prefs['mongodb']['collection'])
    ptoolbar.collnameMenu.setCurrentIndex(index)