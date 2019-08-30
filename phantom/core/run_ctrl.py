import json

from collections import OrderedDict
from itertools import islice

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread

from phantom.database import uploadScriptThread, mongoose_thread

from phantom.applicationSettings import settings

'''
run_cript:
run script to load files into the database
'''
class RunCtrl():
    def __init__(self, parent=None):
        self.parent = parent
        self.__uploadThread = None
        self.__mongooseThread = None

    def __runScript(self, script_s):
        self.parent.getMainToolbar().setRunState(True)
        self.parent.runs += 1
        settings.__LOG__.logInfo("Checking Database Connection...")

        settings.__LOG__.logInfo("Connected to Database. " + settings.__DATABASE__.getDatabaseName() + " collection " + settings.__DATABASE__.getCollectionName())
        self.parent.appendToBoard("Connected to Database. " + settings.__DATABASE__.getDatabaseName() + " collection " + settings.__DATABASE__.getCollectionName())

        self.__mongooseThread = mongoose_thread(settings.__DATABASE__) # instanciate the Q object
        self.__uploadThread = uploadScriptThread(script_s, settings.__DATABASE__,
                                         self.parent.getEditorWidget().getCluster().getPhmScripts()["__dmi_instr__"]["instr"]) # instanciate the Q object

        thread1 = QThread(self.parent) # create a thread
        thread2 = QThread(self.parent)

        try:
            self.__mongooseThread.moveToThread(thread2)
            self.__uploadThread.moveToThread(thread1) # send object to its own thread
        except Exception as err:
            settings.__LOG__.logError("RUN_ERR: error moving to thread")
            self.parent.getMainToolbar().setRunState(False)
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
            script_s = self.parent.getEditorWidget().getEditorTabs().currentWidget().getCurrScript().getScript()

        elif opt == 1:
            script_s = self.parent.getEditorWidget().getCluster().getPhmScripts()

        elif opt == 2:
            clust = self.parent.getEditorWidget().getCluster().getPhmScripts()
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
        self.parent.appendToBoard(msg)
        self.parent.completedRunCounter += 1
        self.parent.getMainToolbar().setRunState(False)
        self.scriptUploadDone("Upload")
        thread.exit(1)

    def scriptUploadDone(self, name):
        self.parent.body.statusBar().showMessage(name + " Complete")
        self.parent.progressBar.setValue(0)

    def setProgressMax(self, mx):
        self.parent.progressBar.setMaximum(mx)

    def updateStatus(self, status):
        self.parent.progressBar.setValue(self.parent.progressBar.value()+1)
        self.parent.body.statusBar().showMessage(status)

    def updateBoard(self, status):
        self.parent.appendToBoard(status)
