import json
import time

from collections import OrderedDict

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread

class upload_thread(QObject):

    update = pyqtSignal(str) # signal data ready to be appended to th board
    done = pyqtSignal(str) # done signal

    def __init__(self, script_s, dbHandler, log):
        QObject.__init__(self)
        self.script_s = script_s
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

        # if self.filePath == None: # dont do because user may want to run script with out saving handle in main and add functionality for this situation
        #     self.stop()
        #     self.done.emit(thread_id)
        #     return
        if isinstance(self.script_s, str):
            self.__run_script(self.script_s)

        elif isinstance( self.script_s, OrderedDict):
            for key, value in self.script_s.items():
                self.__run_script(value.get_script())

        # self.update.emit("Finished")
        self.done.emit(str(self.thread_id) + ": Run Complete.")
        time.sleep(1)

    def __run_script(self, script):
            data = json.loads(script)
            i = 0
            while i < len(data):
                if self.stopFlag:
                    return
                elif not self.pauseFlag:
                    self.dbHandler.insertDoc(data[i])
                    self.update.emit(str(self.thread_id) + ": Sending Objects to Database... %d/%d" %(i+1, len(data)))
                    time.sleep(1)
                    i += 1
                    # print(1)
                else:
                    continue

    # def updateSignal(self, msg):
    #     self.update.emit(msg)
    def setStopFlag(self):
        self.log.logInfo(str(self.thread_id) + ": Run Terminated Before Completion")
        self.done.emit(str(self.thread_id) + ": Run Terminated Before Completion")
        self.stopFlag = True

    def togglePauseFlag(self):
        self.pauseFlag = not self.pauseFlag
  