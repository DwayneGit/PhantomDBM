"""-*- coding: utf-8 -*- """

from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QSize, pyqtSlot, QUrl
from PyQt5.QtWidgets import QAction, QWidget, QSizePolicy

from phantom.database import DatabaseHandler

from phantom.phtm_widgets import PhtmToolBar, PhtmComboBox, PhtmPlainTextEdit, PhtmAction

from phantom.application_settings import settings

class main_tool_bar():
    """ application toolbars class """
    def __init__(self, file_handler, parent):
        self.parent = parent

        self.instr_filepath = None
        self.instr_filename = None

        self.file_handler = file_handler

        self.isRunning = False
        self.isPaused = True

    def setUpToolBar(self):
        #------------------ Top Toolbar ----------------------------
        topTBar = PhtmToolBar()
        topTBar.setMovable(False)

        tbadd = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_add, "Add Script", self.parent)
        tbadd.triggered.connect(self.parent.get_editor_widget().add_new_script)
        topTBar.addAction(tbadd)

        tbsave = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_save, "Save", self.parent)
        tbsave.triggered.connect(lambda: self.file_handler.save_phm())
        topTBar.addAction(tbsave)

        tbphm = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_import_file, "Open PHM", self.parent)
        tbphm.triggered.connect(lambda:self.file_handler.load_phm())
        topTBar.addAction(tbphm)

        tbfiles = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_export, "Export Script", self.parent)
        tbfiles.triggered.connect(lambda: self.file_handler.export_script())
        topTBar.addAction(tbfiles)

        tbsettings = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_settings, "Settings", self.parent)
        tbsettings.triggered.connect(self.parent.showPref)
        topTBar.addAction(tbsettings)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        topTBar.addWidget(spacer)

        tbinfo = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_info, "Info", self.parent)
        tbinfo.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM/wiki")))
        topTBar.addAction(tbinfo)

        # ----------------- Side Toolbar ---------------------------
        sideTBar = PhtmToolBar()
        sideTBar.setMovable(False)

        blank = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_app_icon, "", self.parent)
        blank.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/DwayneGit/PhantomDBM")))
        sideTBar.addAction(blank)

        self.tbrun = QAction()
        self.setRunBtnAction(False)
        sideTBar.addAction(self.tbrun)

        settings.style_signal.icon_signal.connect(lambda: self.setRunBtnAction(self.isRunning))

        tbstop = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_stop, "Stop Run", self.parent)
        tbstop.triggered.connect(lambda: self.setIsRunning(self.parent.r_ctrl.stopRun(self.isRunning)))
        sideTBar.addAction(tbstop)

        self.curr_dmi = PhtmPlainTextEdit(self.parent.get_editor_widget().get_cluster().get_phm_scripts()["__dmi_instr__"]["name"])
        self.curr_dmi.setObjectName("dmi_edit")
        self.curr_dmi.setFixedSize(QSize(175, 31))
        self.curr_dmi.setReadOnly(True)
        self.curr_dmi.mouseDoubleClickEvent = self.__open_dmi_prefs
        sideTBar.addWidget(self.curr_dmi)

        # tbload = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_load_file), "load", self.parent)
        # # tbload.triggered.connect()
        # sideTBar.addAction(tbload)

        # tbedit = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_edit), "edit", self.parent)
        # # tbedit.triggered.connect()
        # sideTBar.addAction(tbedit)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # toolBar is a pointer to an existing toolbar
        sideTBar.addWidget(spacer)

        tbreload = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_sync, "Sync To Client", self.parent)
        tbreload.triggered.connect(self.parent.reloadDbNames)
        sideTBar.addAction(tbreload)

        dropdownSize = QSize(175, 31)

        self.dbnameMenu = PhtmComboBox()
        self.dbnameMenu.setFixedSize(dropdownSize)
        self.dbnameMenu.addItems(DatabaseHandler.getDatabaseList(settings.__DATABASE__.get_host_name(), settings.__DATABASE__.get_port_number()))

        index = self.dbnameMenu.findText(settings.__DATABASE__.get_database_name())
        self.dbnameMenu.setCurrentIndex(index)
        self.dbnameMenu.currentTextChanged.connect(lambda: self.databaseNameChanged())

        sideTBar.addWidget(self.dbnameMenu)

        self.collnameMenu = PhtmComboBox()
        self.collnameMenu.setFixedSize(dropdownSize)
        try:
            self.collnameMenu.addItems(DatabaseHandler.getCollectionList(settings.__DATABASE__.get_host_name(), settings.__DATABASE__.get_port_number(), settings.__DATABASE__.get_database_name()))
        except:
            settings.__LOG__.logError("No collections found in database")

        index = self.collnameMenu.findText(settings.__DATABASE__.get_collection_name())
        self.collnameMenu.setCurrentIndex(index)
        self.collnameMenu.currentTextChanged.connect(lambda: self.collectionNameChanged())
        
        sideTBar.addWidget(self.collnameMenu)

        # tbalert = PhtmAction(settings.style_signal.icon_signal, settings.__ICONS__.get_warning, "Schema Alert", self.parent)
        # tbalert.triggered.connect(lambda: print())
        # sideTBar.addAction(tbalert)

        self.parent.body.addToolBar(Qt.TopToolBarArea, sideTBar)
        self.parent.body.addToolBar(Qt.LeftToolBarArea, topTBar)

    def set_instructions(self):
        self.instr_filename, self.instr_filepath = self.file_handler.load_instructions()
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

    @pyqtSlot()
    def setRunBtnAction(self, state):
        if not state:
            self.setRunBtnIcon(QIcon(settings.__ICONS__.get_play()))
            self.tbrun.setIconText("run")
            # if self.parent.runs > 0:
            #     self.tbrun.triggered.disconnect()
            self.tbrun.triggered.connect(self.__run)

        elif state:
            self.setRunBtnIcon(QIcon(settings.__ICONS__.get_pause()))
            self.tbrun.setIconText("pause")
            self.tbrun.triggered.disconnect()
    #         self.tbrun.triggered.connect(self.pauseRun)

    def __run(self): 
        if self.parent.get_editor_widget().get_editor_tabs().currentWidget():
            self.parent.r_ctrl.run(0)

    def databaseNameChanged(self):
        self.reloadCollectionNames()
        settings.__DATABASE__.set_database_name(self.dbnameMenu.currentText())

    def collectionNameChanged(self):
        settings.__DATABASE__.set_collection_name(self.collnameMenu.currentText())

    def reloadCollectionNames(self):
        self.collnameMenu.currentTextChanged.disconnect()
        self.collnameMenu.clear()

        self.collnameMenu.addItems(DatabaseHandler.getCollectionList(settings.__DATABASE__.get_host_name(), settings.__DATABASE__.get_port_number(), self.dbnameMenu.currentText()))
        self.collnameMenu.currentTextChanged.connect(lambda: self.collectionNameChanged())

        index = self.collnameMenu.findText(settings.__DATABASE__.get_collection_name())
        self.collnameMenu.setCurrentIndex(index)
