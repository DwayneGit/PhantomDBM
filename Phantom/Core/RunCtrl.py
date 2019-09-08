import json

from collections import OrderedDict
from itertools import islice

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget

from Phantom.Database import UploadScriptThread, MongooseThread

from Phantom.ApplicationSettings import Settings

'''
run_cript:
run script to load files into the database
'''
class RunCtrl(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.boardSignal = parent.boardSignal
        self.statusSignal = parent.statusBarSignal
        self.progressSignal = parent.progressSignal
        self.progressMaxSignal = parent.progressMaxSignal

        self.__mainToolbar = None
        self.__editorWidget = None

        self.__uploadThread = None
        self.__mongooseThread = None

    def setMainToolbar(self, mainToolbar):
        self.__mainToolbar = mainToolbar

    def setEditorWidget(self, editorWidget):
        self.__editorWidget = editorWidget

    def __runScript(self, script_s):
        self.__mainToolbar.setRunState(True)
        # self.parent.runs += 1
        Settings.__LOG__.logInfo("Checking Database Connection...")

        Settings.__LOG__.logInfo("Connected to Database. " + Settings.__DATABASE__.getDatabaseName() + " collection " + Settings.__DATABASE__.getCollectionName())
        self.boardSignal.emit("Connected to Database. " + Settings.__DATABASE__.getDatabaseName() + " collection " + Settings.__DATABASE__.getCollectionName())

        self.__mongooseThread = MongooseThread() # instanciate the Q object
        self.__uploadThread = UploadScriptThread(script_s, self.__editorWidget.getCluster().getPhmScripts()["__dmi_instr__"]["instr"]) # instanciate the Q object

        thread1 = QThread(self) # create a thread
        thread2 = QThread(self)

        try:
            self.__mongooseThread.moveToThread(thread2)
            self.__uploadThread.moveToThread(thread1) # send object to its own thread
        except Exception as err:
            Settings.__LOG__.logError("RUN_ERR: error moving to thread")
            self.__mainToolbar.setRunState(False)
            return False

        self.__uploadThread.start.connect(self.setProgressMax)
        self.__uploadThread.updateStatus.connect(self.updateStatus) # link signals to functions
        self.__uploadThread.updateBoard.connect(self.updateBoard) # link signals to functions
        self.__uploadThread.done.connect(self.scriptUploadDone)
        self.__uploadThread.threadDone.connect(lambda msg: self.threadDone(thread1, msg))

        thread1.started.connect(self.__uploadThread.addToDatabase) # connect function to be started in thread
        thread2.started.connect(self.__mongooseThread.insertDocs)

        thread2.start()
        thread1.start()

    def run(self, opt=0, index=None):
        if opt == 0:
            script_s = self.__editorWidget.getEditorTabs().currentWidget().getCurrScript().getScript()

        elif opt == 1:
            script_s = self.__editorWidget.getCluster().getPhmScripts()

        elif opt == 2:
            clust = self.__editorWidget.getCluster().getPhmScripts()
            script_s = OrderedDict(islice(clust.items(), index, len(clust)))

        self.__runScript(script_s)

    def stopRun(self, runState):
        if runState:
            self.__uploadThread.setStopFlag()
            return False

    def pauseRun(self, mainToolbar, runState):
        self.__uploadThread.togglePauseFlag()
        if runState:
            mainToolbar.setRunBtnIcon(QIcon("icons/play_pause.png"))
            return False
        mainToolbar.setRunBtnIcon(QIcon("icons/pause.png"))
        return True

    def threadDone(self, thread, msg):
        self.boardSignal.emit(msg)
        # self.parent.completedRunCounter += 1
        self.__mainToolbar.setRunState(False)
        self.scriptUploadDone("Upload")
        thread.exit(1)

    def scriptUploadDone(self, name):
        self.statusSignal.emit(name + " Complete", 2000)
        self.progressSignal.emit(0)

    def setProgressMax(self, mx):
        self.progressMaxSignal.emit(mx)

    def updateStatus(self, status):
        self.progressSignal.emit(-1)
        self.statusSignal.emit(status, 2000)

    def updateBoard(self, status):
        self.boardSignal.emit(status)
