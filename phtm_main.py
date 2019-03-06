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
from DBConnection import *
from phtm_tool_bar import phtm_tool_bar, reloadCollectionNames
from Center import center_window

import style.style_template as styles

from phtm_title_bar import phtm_title_bar

from file_ctrl import tmpScriptCleaner
import run_ctrl as r_ctrl
import file_ctrl as f_ctrl
from phtm_logger import phtm_logger

BUFFERSIZE = 1000

class Manager(QMainWindow):
    def __init__(self):
        super().__init__()
        #set window icon
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(script_dir + os.path.sep + 'icons/phantom.png'))

        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 520

        self.oldPos = self.pos()

        # self.__layout = QVBoxLayout()
        self.layout().setSpacing(0) 

        self.title_bar = phtm_title_bar(self, True)
        self.title_bar.generate_title_bar()

        self.addToolBar(Qt.TopToolBarArea, self.title_bar)

        self.main_window = main_window(self)
        self.main_window.statusBar().showMessage("Ready")

        self.setCentralWidget(self.main_window)
        # self.setStyleSheet("""
        #     Manager {
        #         background-color: rgb(46, 51, 58);
        #         color: white;
        #         border-style: none;
        #     }
        # """)

        # self.setLayout(self.__layout)

        self.setGeometry(self.left, self.top, self.width, self.height) # set screen size (left, top, width, height
        self.move(center_window(self))


class main_window(styles.phtm_main_window):
    __runs = 0
    __completedRuns = 0
    def __init__(self, parent=None):
        super().__init__(style="ghost")

        self.dmi_settings = None
        self.parent = parent
        # self.__oldPos = QPoint

        self.log = phtm_logger()
        self.log.logInfo("Program Started.")

        self.prefs = Preferences('config', prefDict=DefaultGeneralConfig.prefDict, log=self.log) # name of preference file minus json
        self.prefs.loadConfig()

        self.icon_set=styles.phtm_icons()

        f_ctrl.tmpScriptCleaner(self)

        self.dbData = self.prefs.prefDict['mongodb']

        self.isRunning = False
        self.isPaused = True

        login = loginScreen()
        if login.exec_():
            self.log.logInfo("Successfully Logged In.")
            self.user = login.user
            self.initUI()
        else:
            self.log.logInfo("No login program exited.")
            sys.exit()

    def initUI(self):
        '''
        initiates application UI
		'''
        self.progTitle = 'Phantom DBM'
        self.currTitle = self.progTitle

        self.parent.setWindowTitle(self.progTitle)
        self.parent.setWindowIcon(QIcon('icons/phantom.png'))

        splitter1 = QSplitter(Qt.Horizontal)


        # Add text field
        self.brd = styles.phtm_plain_text_edit()
        self.brd.setReadOnly(True)
        self.brd.insertPlainText("Welcome to Phantom Database Manager (DBM).")
        # self.brd.move(10,10)
        # self.brd.resize(self.width-60,self.height-20)

        self.fileLoaded = True
        self.filePath = None

        self.fileContents = styles.phtm_text_edit()
        self.fileContents.setText("[\n    {\n        \"\": \"\"\n    }\n]")
        self.fileContents.textChanged.connect(self.isChanged)

        self.changed = False
        # check if file is loaded and set flag to use to ask if save necessary before running or closing
        splitter1.addWidget(self.brd)
        splitter1.addWidget(self.fileContents)

        self.setCentralWidget(splitter1)

        splitter1.setSizes([300,212])
        # self.setStatusBar(StatusBar())
        self.statusBar().showMessage('Ready')
        self.statusBar().setFixedHeight(20)

        self.progressBar = QProgressBar()

        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setFixedWidth(200)

        self.phtm_tool_bar = phtm_tool_bar(self, self.icon_set)
        self.phtm_tool_bar.setUpToolBar()
        
        self.menu_bar = phtm_menu_bar(self)
        self.menu_bar.init_menu_bar()

        self.setMenuWidget(self.menu_bar)
 
        self.show()

    def isChanged(self):
        if not self.changed:
            self.changed = True
            self.parent.setWindowTitle("* " + self.currTitle)

    def editWindowTitle(self):
        # use regex to grab the name of the file from the path and added to title
        newTitle = self.progTitle
        fileName = re.split('^(.+)\/([^\/]+)$', self.filePath)
        newTitle = newTitle +  " - " + fileName[2]
        self.parent.setWindowTitle(newTitle)
        self.currTitle = newTitle

    def setRunState(self, state):
        self.setIsRunning(state)
        self.setRunBtnAction(state)

    def setIsRunning(self, state):
        self.isRunning = state
    
    def setRunBtnIcon(self, icon):
        self.phtm_tool_bar.tbrun.setIcon(icon)

    def setRunBtnAction(self, state):
        if state == False:
            self.setRunBtnIcon(QIcon(self.icon_set.play))
            self.phtm_tool_bar.tbrun.setIconText("run")
            if main_window.__runs > 0:
                self.phtm_tool_bar.tbrun.triggered.disconnect()
            self.phtm_tool_bar.tbrun.triggered.connect(lambda: r_ctrl.runScript(self, main_window.__runs, main_window.__completedRuns))

        elif state == True: 
            self.setRunBtnIcon(QIcon("icons/pause.png"))
            self.phtm_tool_bar.tbrun.setIconText("pause")
            self.phtm_tool_bar.tbrun.triggered.disconnect()
    #         self.phtm_tool_bar.tbrun.triggered.connect(self.pauseRun)

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
        p = PreferencesDialog(self.user, self.log)
        p.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        p.setAttribute(Qt.WA_NoSystemBackground)
        p.setAttribute(Qt.WA_TranslucentBackground)
        # print(self.prefs.prefDict)
        if p.exec_():
            self.prefs.loadConfig()
            self.dbData = self.prefs.prefDict['mongodb']
            
            self.reloadDbNames()
            reloadCollectionNames(self.phtm_tool_bar, self)

        else:
            pass

    def reloadDbNames(self):
        self.phtm_tool_bar.dbnameMenu.clear()
        self.phtm_tool_bar.dbnameMenu.addItems(DatabaseHandler.getDatabaseList(self.dbData['host'], self.dbData['port']))
        index = self.phtm_tool_bar.dbnameMenu.findText(self.prefs.prefDict['mongodb']['dbname'])
        self.phtm_tool_bar.dbnameMenu.setCurrentIndex(index)

    # def mousePressEvent(self, evt):
    #     self.__oldPos = evt.globalPos()
        
    # def mouseMoveEvent(self, evt):
    #     delta = QPoint()
    #     delta  = evt.globalPos() - self.__oldPos
    #     move(x()+delta.x(), y()+delta.y())
    #     self.__oldPos = evt.globalPos()

if __name__ == '__main__':
    
    APP = QApplication(sys.argv)

    MANAGER = Manager()
    MANAGER.setWindowFlags(Qt.FramelessWindowHint)
    MANAGER.show()
    sys.exit(APP.exec_())

