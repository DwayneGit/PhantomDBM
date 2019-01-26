import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from Center import center_window
from Dialogs import *
from Preferences import *
from Users import *
from DBConnection import *
import logging
import json
import threading
import time
import re
import pprint

class Manager(QMainWindow):
    
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

        # login = loginScreen()
        # if login.exec_():
        #     self.user = login.user
        self.prefs = Preferences('config', prefDict = DefaultGeneralConfig.prefDict) # name of preference file minus json
        self.prefs.loadConfig()
        # print(self.prefs)
        self.dbData = self.prefs.prefDict['mongodb']

        login = loginScreen()
        if login.exec_():
            self.user = login.user
            self.initUI()
            self.move(center_window(self))
        else:
            self.reject()
        
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
        self.b = QPlainTextEdit(self)
        self.b.setReadOnly(True)
        self.b.insertPlainText("Welcome to Phantom Database Manager (DBM).")
        # self.b.move(10,10)
        # self.b.resize(self.width-60,self.height-20)

        self.fileLoaded = True
        self.filePath = None

        self.fileContents = QTextEdit()
        self.fileContents.textChanged.connect(self.isChanged)
        self.changed = False 
        # check if file is loaded and set flag to use to ask if save necessary before running or closing
        splitter1.addWidget(self.b)
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
        
        tbfile = QAction(QIcon("import-file.png"),"import",self)
        tbfile.triggered.connect(self.getfile)
        topTBar.addAction(tbfile)
        
        tbsave = QAction(QIcon("save.png"),"save",self)
        tbsave.triggered.connect(self.saveScript)
        topTBar.addAction(tbsave)
            
        tbfiles = QAction(QIcon("export-file.png"),"export",self)
        tbfiles.triggered.connect(self.exportScript)
        topTBar.addAction(tbfiles)
        
        tbrun = QAction(QIcon("play.png"),"run",self)
        tbrun.triggered.connect(self.runScript)
        topTBar.addAction(tbrun)
            
        tbpause = QAction(QIcon("pause.png"),"pause",self)
        # tbpause.triggered.connect(self.getfiles)
        topTBar.addAction(tbpause)

        tbstop = QAction(QIcon("stop.png"),"stop",self)
        # tbpause.triggered.connect(self.getfiles)
        topTBar.addAction(tbstop)



        # ----------------- Side Toolbar ---------------------------
        sideTBar = QToolBar(self)
        
        tbopen = QAction(QIcon("internet.png"),"open",self)
        # tbopen.triggered.connect()
        sideTBar.addAction(tbopen)
        
        tbload = QAction(QIcon("load-file.png"),"open",self)
        tbload.triggered.connect(self.startExplorer)
        sideTBar.addAction(tbload)
        
        tbedit = QAction(QIcon("editor.png"),"open",self)
        # tbedit.triggered.connect()
        sideTBar.addAction(tbedit)
        
        tbsettings = QAction(QIcon("settings.png"),"open",self)
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
            quit_msg = "Changes made will be saved.\nAre you sure you want to run this script?"
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

        
        running = True
        connected = False

        r, w = os.pipe()

        self.b.appendPlainText("Checking Database Connection...")
        dbHandler = DatabaseHandler(self.dbData)
        if dbHandler.serverStatus() == True:

            self.b.appendPlainText("Connected to Dabase.")
            
            try:
                thread.start_new_thread(self.addToDatabase)

            try:
                newpid = os.fork()
            except OSError:
                print("error in fork")

            if newpid == 0:
                os.close(r)
                w = os.fdopen(w,'w')
                w.write("Running JSON Script...")

                with open(self.filePath) as infile:
                    data = json.load(infile)
                    for i in range(len(data)):
                        dbHandler.insertDoc(data[i])
                        w.write("Sending Objects to Database... %d/%d" %(i+1,len(data)))
                        print(1)
                        time.sleep(1)

                w.write("Finished")

                self.statusBar().showMessage('Ready')

                w.close()
                    
                print(str(running) + " 2")
                os._exit(0)

        else:
            self.b.appendPlainText("Failed to Connect to Database")
            return

        os.close(w)
        r = os.fdopen(r)
        
        while True:
            print("parent")
            message = r.read()
            if not message:
                break
            
            self.b.appendPlainText(message)

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
            
def addToDatabase(self, threading.Thread):

    os.close(r)
    w = os.fdopen(w,'w')
    w.write("Running JSON Script...")
    # sys.stdout.flush()

    with open(filePath) as infile:
        data = json.load(infile)
        for i in range(len(data)):
            dbHandler.insertDoc(data[i])
            w.write("Sending Objects to Database... %d/%d" %(i+1,len(data)))
            print(1)
            time.sleep(1)
            

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setStyle("plastique")
    manager = Manager()
    manager.statusBar().showMessage("Ready")    
    sys.exit(app.exec_())

