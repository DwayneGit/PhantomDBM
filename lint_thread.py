import json
import time

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread

class upload_thread(QObject):

    update = pyqtSignal(str) # signal data ready to be appended to th board
    done = pyqtSignal(str) # done signal

    def __init__(self, filePath, dbHandler, log):
        QObject.__init__(self)
        self.filePath = filePath
        self.dbHandler = dbHandler
        self.pauseFlag = False
        self.stopFlag = False
        self.log = log

    @pyqtSlot()
    def addToDatabase(self):

        # thread_name = QThread.currentThread().objectName()
        self.thread_id = int(QThread.currentThreadId())  # cast to int() is necessary

        # print("Opening Child FIFO...")
        self.log.logInfo(str(self.thread_id) + ": Running JSON Script...")
        time.sleep(1)

        # self.update.emit("Finished")
        self.done.emit(str(self.thread_id) + ": Run Complete.")
        time.sleep(1)

    # def updateSignal(self, msg):
    #     self.update.emit(msg)
    def setStopFlag(self):
        self.log.logInfo(str(self.thread_id) + ": Run Terminated Before Completion")
        self.done.emit(str(self.thread_id) + ": Run Terminated Before Completion")
        self.stopFlag = True

    def togglePauseFlag(self):
        self.pauseFlag = not self.pauseFlag
  