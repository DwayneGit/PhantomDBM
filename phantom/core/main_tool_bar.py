"""-*- coding: utf-8 -*- """

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QAction, QWidget, QSizePolicy

from phantom.database import database_handler

from phantom.phtm_widgets import PhtmToolBar
from phantom.phtm_widgets import PhtmComboBox
from phantom.phtm_widgets import PhtmPlainTextEdit

from phantom.file_stuff import file_ctrl as f_ctrl

class main_tool_bar():
    """ application toolbars class """
    def __init__(self, parent, icon_set):
        self.parent = parent
        self.icon_set = icon_set

        self.instr_filepath = None
        self.instr_filename = None

        self.isRunning = False
        self.isPaused = True

    def setUpToolBar(self):
        #------------------ Top Toolbar ----------------------------
        topTBar = PhtmToolBar()

        tbfile = QAction(QIcon(self.icon_set.import_file),"import",self.parent)
        tbfile.triggered.connect(self.parent.get_editor_widget().load_script)
        topTBar.addAction(tbfile)

        tbsave = QAction(QIcon(self.icon_set.save),"save",self.parent)
        tbsave.triggered.connect(lambda: f_ctrl.save_script(self.parent.get_editor_widget().get_editor_tabs().currentWidget(), self.parent.get_editor_widget()))
        topTBar.addAction(tbsave)

        tbfiles = QAction(QIcon(self.icon_set.export_file),"export",self.parent)
        tbfiles.triggered.connect(lambda: f_ctrl.export_script(self.parent.get_editor_widget().get_editor_tabs().currentWidget().toPlainText()))
        topTBar.addAction(tbfiles)

        self.tbrun = QAction()
        self.setRunBtnAction(False)
        topTBar.addAction(self.tbrun)

        tbstop = QAction(QIcon(self.icon_set.stop),"stop",self.parent)
        tbstop.triggered.connect(lambda: self.setIsRunning(self.parent.r_ctrl.stopRun(self.isRunning)))
        topTBar.addAction(tbstop)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        topTBar.addWidget(spacer)

        self.curr_dmi = PhtmPlainTextEdit(self.parent.get_editor_widget().get_cluster().get_phm_scripts()["__dmi_instr__"]["name"])
        self.curr_dmi.setFixedSize(QSize(175, 31))
        self.curr_dmi.setReadOnly(True)
        self.curr_dmi.mouseDoubleClickEvent = self.__open_dmi_prefs
        topTBar.addWidget(self.curr_dmi)

        # ----------------- Side Toolbar ---------------------------
        sideTBar = PhtmToolBar()
        tbload = QAction(QIcon(self.icon_set.load_file), "load", self.parent)
        # tbload.triggered.connect()
        sideTBar.addAction(tbload)

        tbedit = QAction(QIcon(self.icon_set.edit), "edit", self.parent)
        # tbedit.triggered.connect()
        sideTBar.addAction(tbedit)

        tbsettings = QAction(QIcon(self.icon_set.settings), "settings", self.parent)
        tbsettings.triggered.connect(self.parent.showPref)
        sideTBar.addAction(tbsettings)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # toolBar is a pointer to an existing toolbar
        sideTBar.addWidget(spacer)

        tbreload = QAction(QIcon(self.icon_set.reload), "reload", self.parent)
        tbreload.triggered.connect(self.parent.reloadDbNames)
        sideTBar.addAction(tbreload)

        dropdownSize = QSize(175, 31)

        self.dbnameMenu = PhtmComboBox()
        self.dbnameMenu.setFixedSize(dropdownSize)
        self.dbnameMenu.addItems(database_handler.getDatabaseList(self.parent.dbData['host'], self.parent.dbData['port'], self.parent.log))

        index = self.dbnameMenu.findText(self.parent.prefs['mongodb']['dbname'])
        self.dbnameMenu.setCurrentIndex(index)
        self.dbnameMenu.currentTextChanged.connect(lambda: databaseNameChanged(self, self.parent))

        sideTBar.addWidget(self.dbnameMenu)

        self.collnameMenu = PhtmComboBox()
        self.collnameMenu.setFixedSize(dropdownSize)
        try:
            self.collnameMenu.addItems(database_handler.getCollectionList(self.parent.dbData['host'], self.parent.dbData['port'], self.parent.dbData['dbname']))
        except:
            self.parent.log.logError("No collections found in database")

        index = self.collnameMenu.findText(self.parent.prefs['mongodb']['collection'])
        self.collnameMenu.setCurrentIndex(index)
        self.collnameMenu.currentTextChanged.connect(lambda: collectionNameChanged(self, self.parent))
        sideTBar.addWidget(self.collnameMenu)

        self.parent.addToolBar(Qt.TopToolBarArea, topTBar)
        self.parent.addToolBarBreak(Qt.TopToolBarArea)
        self.parent.addToolBar(Qt.TopToolBarArea, sideTBar)

    def set_instructions(self):
        self.instr_filename, self.instr_filepath = f_ctrl.load_instructions()
        # print(self.instr_filepath)
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
            self.setRunBtnIcon(QIcon(self.icon_set.play))
            self.tbrun.setIconText("run")
            # if self.parent.runs > 0:
            #     self.tbrun.triggered.disconnect()
            self.tbrun.triggered.connect(self.__run)

        elif state:
            self.setRunBtnIcon(QIcon(self.icon_set.reload))
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