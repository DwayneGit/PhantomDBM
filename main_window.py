import os
import re
import sys
import json
import pprint
import logging

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Users import *
from Dialogs import *
from phtm_menu_bar import phtm_menu_bar
from Preferences import *
from database.DBConnection import *
from main_tool_bar import main_tool_bar, reloadCollectionNames, databaseNameChanged
from Center import center_window

from phtm_widgets.phtm_icons import phtm_icons
from phtm_widgets.phtm_dialog import phtm_dialog
from phtm_widgets.phtm_tab_widget import phtm_tab_widget
from phtm_widgets.phtm_plain_text_edit import phtm_plain_text_edit

from file.phm_file_handler import phm_file_handler
from phtm_editor import phtm_editor
from phtm_editor_widget import phtm_editor_widget
from file.json_script import json_script

from file_ctrl import tmpScriptCleaner
import run_ctrl as r_ctrl
import file_ctrl as f_ctrl
from phtm_logger import phtm_logger

BUFFERSIZE = 1000

class main_window(QMainWindow):
    __runs = 0
    __completedRuns = 0
    def __init__(self, parent=None):
        super().__init__()

        self.dmi_settings = None
        self.parent = parent
        # self.__oldPos = QPoint

        self.log = phtm_logger()
        self.log.logInfo("Program Started.")

        self.__blank_cluster = phm_file_handler()

        self.prefs = Preferences('config', prefDict=DefaultGeneralConfig.prefDict, log=self.log) # name of preference file minus json
        self.prefs.loadConfig()

        self.icon_set=phtm_icons()

        f_ctrl.tmpScriptCleaner(self)

        self.dbData = self.prefs.prefDict['mongodb']

        self.isRunning = False
        self.isPaused = True

        login = phtm_dialog("Login", QRect(10, 10, 260, 160), self)
        login.set_central_dialog(loginScreen(login))

        if login.exec_():
            self.log.logInfo("Successfully Logged In.")
            self.user = login.central_dialog().user
            self.initUI()
        else:
            self.log.logInfo("No login program exited.")
            sys.exit()

    def initUI(self):
        '''
        initiates application UI
		'''
        self.currTitle = self.parent.window_title

        self.parent.setWindowIcon(QIcon('icons/phantom.png'))

        splitter1 = QSplitter(Qt.Horizontal)


        # Add text field
        self.brd = phtm_plain_text_edit()
        self.brd.setReadOnly(True)
        self.brd.insertPlainText("Welcome to Phantom Database Manager (DBM).")
        # self.brd.move(10,10)
        # self.brd.resize(self.width-60,self.height-20)

        self.fileLoaded = True
        self.filePath = None

        # self.fileContents = phtm_editor()
        # self.fileContents.setPlainText("[\n    {\n        \"\": \"\"\n    }\n]")
        # self.fileContents.textChanged.connect(self.isChanged)

        # self.editor_tabs = phtm_tab_widget(self)
        # self.editor_tabs.add_editor()

        # self.editor_tabs.setMovable(True)
        # self.editor_tabs.setTabsClosable(True)

        self.__editor_widget = phtm_editor_widget(self)

        self.changed = False
        # check if file is loaded and set flag to use to ask if save necessary before running or closing
        splitter1.addWidget(self.brd)
        splitter1.addWidget(self.__editor_widget)

        self.setCentralWidget(splitter1)

        splitter1.setSizes([300, 325])
        # self.setStatusBar(StatusBar())
        self.statusBar().showMessage('Ready')
        self.statusBar().setFixedHeight(20)

        self.progressBar = QProgressBar()

        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setFixedWidth(200)

        self.main_tool_bar = main_tool_bar(self, self.icon_set)
        self.main_tool_bar.setUpToolBar()
        
        self.menu_bar = phtm_menu_bar(self)
        self.menu_bar.init_menu_bar()

        self.setMenuWidget(self.menu_bar)
 
        self.show()

    def set_window_title(self, text):
        self.parent.set_window_title(text)
    
    def getWindowTitle(self):
        return self.parent.getWindowTitle()

    # def isChanged(self):
    #     if not self.changed:
    #         self.changed = True
    #         self.set_window_title("* " + self.currTitle)

    def updateWindowTitle(self, newTitle):
        self.set_window_title(newTitle + " - " + self.parent.getPermanentTitle())

    def setRunState(self, state):
        self.setIsRunning(state)
        self.setRunBtnAction(state)

    def setIsRunning(self, state):
        self.isRunning = state
    
    def setRunBtnIcon(self, icon):
        self.main_tool_bar.tbrun.setIcon(icon)

    def setRunBtnAction(self, state):
        if state == False:
            self.setRunBtnIcon(QIcon(self.icon_set.play))
            self.main_tool_bar.tbrun.setIconText("run")
            if main_window.__runs > 0:
                self.main_tool_bar.tbrun.triggered.disconnect()
            self.main_tool_bar.tbrun.triggered.connect(lambda: r_ctrl.run_script(self, main_window.__runs, main_window.__completedRuns))

        elif state == True: 
            self.setRunBtnIcon(QIcon("icons/pause.png"))
            self.main_tool_bar.tbrun.setIconText("pause")
            self.main_tool_bar.tbrun.triggered.disconnect()
    #         self.main_tool_bar.tbrun.triggered.connect(self.pauseRun)

    #create custom signal to ubdate UI
    @pyqtSlot(str)
    def appendToBoard(self, message):
        # self.log.logInfo(message)
        self.brd.appendHtml(message)
        QCoreApplication.processEvents()


    def closeEvent(self, event):
        if self.changed:
            quit_msg = "Your changes have not been saved.\nAre you sure you want to exit the program?"
            reply = QMessageBox.question(self, 'Message', 
                            quit_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            self.log.logInfo("Program Ended")

    def showPref(self):
        p = phtm_dialog("Preferences", QRect(10, 10, 350, 475), self)
        p.set_central_dialog(preference_body(self.user, self.log, p))
        
        # print(self.prefs.prefDict)
        if p.exec_():
            self.prefs = p.prefs
            self.dbData = self.prefs.prefDict['mongodb']
            self.main_tool_bar.curr_dmi.setPlainText(self.prefs.prefDict["dmi"]["filename"])
            self.reloadDbNames()
            # reloadCollectionNames(self.main_tool_bar, self)

        else:
            pass

    def reloadDbNames(self):
        self.main_tool_bar.dbnameMenu.currentTextChanged.disconnect()
        self.main_tool_bar.dbnameMenu.clear()
        
        self.main_tool_bar.dbnameMenu.addItems(database_handler.getDatabaseList(self.dbData['host'], self.dbData['port']))
        self.main_tool_bar.dbnameMenu.currentTextChanged.connect(lambda: databaseNameChanged(self.main_tool_bar, self))
        
        index = self.main_tool_bar.dbnameMenu.findText(self.prefs.prefDict['mongodb']['dbname'])
        self.main_tool_bar.dbnameMenu.setCurrentIndex(index)

    def get_editor_widget(self):
        return self.__editor_widget

    # def mousePressEvent(self, evt):
    #     self.__oldPos = evt.globalPos()
        
    # def mouseMoveEvent(self, evt):
    #     delta = QPoint()
    #     delta  = evt.globalPos() - self.__oldPos
    #     move(x()+delta.x(), y()+delta.y())
    #     self.__oldPos = evt.globalPos()