
import os
import re
import sys
import json
import time
import errno
import pprint
import logging

from Users import *
from Dialogs import *
from PyQt5.QtGui import * 
from Preferences import *
from DBConnection import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Center import center_window

from Thread import *

bufferSize = 1000

class Manager(QMainWindow):
    __runs = 0
    __completedRuns = 0
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 520

        # self.prefs = Preferences('config', DefaultGeneralConfig.prefDict) # name of preference file minus json
        # self.prefs.loadConfig()

        # self.dbData = self.prefs.prefDict['mongodb']
        #load data from database
        #self.db = DatabaseHandler(self.dbData['collections'], self.dbData['dbname'], self.dbData['host'], self.dbData['port'], tableSize, pageNum) # move to loop and give individual collections
        #print(self.db.mDbDocs)
        
        self.prefs = Preferences('config', prefDict = DefaultGeneralConfig.prefDict) # name of preference file minus json
        self.prefs.loadConfig()
        
        self.dbData = self.prefs.prefDict['mongodb']

        self.isRunning = False
        self.isPaused = True

        login = loginScreen()
        if login.exec_():
            self.user = login.user
            self.initUI()
            self.move(center_window(self))
        else:
            self.reject()

    # @pyqtSlot()
    # def updateBrd():
    #     ''' Give evidence that a bag was punched. '''
    #     print('Bag was punched.')

    def initUI(self):
        '''
        initiates application UI
		'''   
        self.progTitle = 'Phantom DBM'
        self.currTitle = self.progTitle

        self.setWindowTitle(self.progTitle)  
        self.setGeometry(self.left,self.top,self.width, self.height) # set screen size (left, top, width, height

        splitter1 = QSplitter(Qt.Horizontal)

        # Add text field
        self.brd = QPlainTextEdit(self)
        self.brd.setReadOnly(True)
        self.brd.insertPlainText("Welcome to Phantom Database Manager (DBM).")
        # self.brd.move(10,10)
        # self.brd.resize(self.width-60,self.height-20)

        self.fileLoaded = True
        self.filePath = None

        self.fileContents = QTextEdit()
        self.fileContents.setText("[\n    {\n        \"\": \"\"\n    }\n]")
        self.fileContents.textChanged.connect(self.isChanged)
        self.changed = False 
        # check if file is loaded and set flag to use to ask if save necessary before running or closing
        splitter1.addWidget(self.brd)
        splitter1.addWidget(self.fileContents)

        self.setCentralWidget(splitter1)

        splitter1.setSizes([300,200])
        # self.setStatusBar(StatusBar())
        '''
        self.db = DatabaseHandler(self.dbData, pageNum)
        for i in range(len(self.db.mDbCollections)):
            x =[]
            if not(self.db.mDbDocs[i]):
                x=[]
            else:
                for key in self.db.mDbDocs[i][0]:
                    #print(key)
                    x.append(key)
            self.tabWidget.addTab(MainLayout(x), self.db.mDbCollections[i])
        '''

        self.setUpToolBar()
        self.initMenuBar()
 
        self.show()

    def isChanged(self):
        if not self.changed:
            self.changed = True
            self.setWindowTitle("* " + self.currTitle) 

    def initMenuBar(self):
        extractAction = QAction("Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(sys.exit)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(extractAction)

        editMenu = mainMenu.addMenu('Edit')

        helpMenu = mainMenu.addMenu('Help')
        
    def setUpToolBar(self):
        #------------------ Top Toolbar ----------------------------
        topTBar = QToolBar(self)
        
        tbfile = QAction(QIcon("icons/import-file.png"),"import",self)
        tbfile.triggered.connect(self.getfile)
        topTBar.addAction(tbfile)
        
        tbsave = QAction(QIcon("icons/save.png"),"save",self)
        tbsave.triggered.connect(self.saveScript)
        topTBar.addAction(tbsave)
            
        tbfiles = QAction(QIcon("icons/export-file.png"),"export",self)
        tbfiles.triggered.connect(self.exportScript)
        topTBar.addAction(tbfiles)
        
        self.tbrun = QAction()
        self.setRunBtnAction( False)
        topTBar.addAction(self.tbrun)

        tbstop = QAction(QIcon("icons/stop.png"),"stop",self)
        tbstop.triggered.connect(self.stopRun)
        topTBar.addAction(tbstop)



        # ----------------- Side Toolbar ---------------------------
        sideTBar = QToolBar(self)
        
        tbopen = QAction(QIcon("icons/internet.png"),"open",self)
        # tbopen.triggered.connect()
        sideTBar.addAction(tbopen)
        
        tbload = QAction(QIcon("icons/load-file.png"),"open",self)
        tbload.triggered.connect(self.startExplorer)
        sideTBar.addAction(tbload)
        
        tbedit = QAction(QIcon("icons/editor.png"),"open",self)
        # tbedit.triggered.connect()
        sideTBar.addAction(tbedit)
        
        tbsettings = QAction(QIcon("icons/settings.png"),"open",self)
        tbsettings.triggered.connect(self.showPref)
        sideTBar.addAction(tbsettings)

        self.addToolBar(Qt.TopToolBarArea,topTBar)
        self.addToolBar(Qt.RightToolBarArea,sideTBar)

    def startExplorer(self):
        fx = FileDialogDemo()
        fx.exec_()
        
    def putfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
            'c:\\',"Image files (*.jpg *.gif *.png)")
		
    def getfile(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("JSON files (*.json)")
        filenames = []
		
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.filePath = filenames[0] # save file path
            print(self.filePath)
            self.editWindowTitle()
            f = open(filenames[0], 'r')
			
        with f:
            self.fileContents.blockSignals(True)
            data = f.read()
            self.fileContents.setText(data)
            self.changed = False
            self.fileContents.blockSignals(False)

    def editWindowTitle(self):
        # use regex to grab the name of the file from the path and added to title
        newTitle = self.progTitle
        fileName = re.split('^(.+)\/([^\/]+)$', self.filePath)
        newTitle = newTitle +  " - " + fileName[2]
        self.setWindowTitle(newTitle) 
        self.currTitle = newTitle
        print(fileName[2])

    '''
    runScript:
    run script to load files into the database
    '''
    def runScript(self):
        # make sure file is not deleted before saving
        if self.changed:
            quit_msg = "Changes made will be saved.\nAre you sure you want to run this script?\nFunctionality to be implemented."
            reply = QMessageBox.question(self, 'Message', 
                            quit_msg, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                if self.filePath:
                    self.saveScript()
                else:
                    self.exportScript()
            elif reply == QMessageBox.Cancel:
                return   
            else:
                pass
        
        if self.filePath == None:
            print("No File To Run!")
            return

        self.setRunState(True)
        Manager.__runs += 1

        self.appendToBoard("Checking Database Connection...")

        dbHandler = DatabaseHandler(self.dbData)
        if dbHandler.serverStatus() == True:

            self.appendToBoard("Connected to Dabase.")

            self.thread1 = Thread1(self.filePath, dbHandler) # instanciate the Q object
            thread = QThread(self) # create a thread

            self.thread1.moveToThread(thread) # send object to its own thread

            self.thread1.update.connect(self.appendToBoard) # link signals to functions
            self.thread1.done.connect(self.threadDone)
            
            thread.started.connect(self.thread1.addToDatabase) # connect function to be started in thread
            thread.start()
            
            # self.Thread2 = Thread2()
            # self.connect(self.Thread2, SIGNAL("finished()"), self.done)
            # self.Thread2.start()

        else:
            self.appendToBoard("Failed to Connect to Database")
            self.setRunState(False)
            return

    def stopRun(self):
        if self.isRunning:
            self.thread1.setStopFlag()
            self.setIsRunning(False)

    def pauseRun(self):
        if self.isRunning:
            self.setRunBtnIcon(QIcon("icons/play_pause.png"))
            self.setIsRunning(False)
        else:
            self.setRunBtnIcon(QIcon("icons/pause.png"))
            self.setIsRunning(True)

        self.thread1.togglePauseFlag()

    def setRunState(self, state):
        self.setIsRunning(state)
        self.setRunBtnAction(state)

    def setIsRunning(self, state):
        self.isRunning = state
    
    def setRunBtnIcon(self, icon):
        self.tbrun.setIcon(icon)

    def setRunBtnAction(self, state):
        if state == False:
            self.setRunBtnIcon(QIcon("icons/play.png"))
            self.tbrun.setIconText("run")
            if Manager.__runs > 0:
                self.tbrun.triggered.disconnect(self.pauseRun)
            self.tbrun.triggered.connect(self.runScript)

        elif state == True: 
            self.setRunBtnIcon(QIcon("icons/pause.png"))
            self.tbrun.setIconText("pause")
            self.tbrun.triggered.disconnect(self.runScript)
            self.tbrun.triggered.connect(self.pauseRun)

    @pyqtSlot(str)
    def threadDone(self, msg):
        self.appendToBoard(msg)
        Manager.__completedRuns += 1
        self.setRunState(False)

    #create custom signal to ubdate UI
    @pyqtSlot(str)
    def appendToBoard(self, message):
        # print(message)
        self.brd.appendPlainText(message)
        QCoreApplication.processEvents()

    def saveScript(self):
        if not self.filePath:
            self.exportScript()
            return
        self.statusBar().showMessage("Saving File ...")
        # pprint.pprint(re.sub('\'|\n', '', self.fileContents.toPlainText()))
        with open(self.filePath, 'w') as outfile:
            outfile.write(eval(json.dumps(self.fileContents.toPlainText(), indent=4)))
        if self.filePath:
            self.editWindowTitle()
        else:
            self.setWindowTitle(self.currTitle)

        self.changed = False 

    def exportScript(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save File","","JSON files (*.json)")
        if fileName:
            self.filePath = fileName
            self.saveScript()

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
            pass

    def showPref(self):
        p = PreferencesDialog(self.user)
        p.exec_()

    # def setTabs(self):
    #     '''
    #     Create TABS for each collection
    #     '''
    #     self.collectionNames = DatabaseHandler.getCollectionList(self.dbData)

    #     self.tabWidget = QTabWidget(self)
    #     self.tabWidget.setTabPosition(QTabWidget.West)
    #     self.tabWidget.setObjectName('tabWidget')

    #     pageNum = 0
        
    #     print(self.collectionNames)

    #     for i in range(len(self.collectionNames)):
    #         #print(type(self.db.mDbDocs[i]))
    #         self.db = DatabaseHandler(self.dbData, self.collectionNames[i], pageNum)
    #         if not(self.db.mDbDocs): #if collection is empty skip it
    #             continue
    #         self.tabWidget.addTab(MainLayout(self.db), self.db.mDbCollection)

    #     self.setCentralWidget(self.tabWidget)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setStyle("plastique")
    manager = Manager()
    manager.statusBar().showMessage("Ready")    
    sys.exit(app.exec_())

