import json
import time

from collections import OrderedDict

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread
from phantom.instructions import dmi_handler

from phantom.utility import validate_json_script

class upload_thread(QObject):
    update = pyqtSignal(str) # signal data ready to be appended to th board
    start = pyqtSignal(int) # signal data ready to be appended to th board
    done = pyqtSignal(str)

    thrd_done = pyqtSignal(str) # done signal

    def __init__(self, script_s, dbHandler, log, dmi_instr=None):
        QObject.__init__(self)
        self.script_s = script_s
        self.dbHandler = dbHandler
        self.pauseFlag = False
        self.stopFlag = False
        self.log = log

        self.thread_id = int(QThread.currentThreadId())  # cast to int() is necessary

        if dmi_instr:
            self.dmi = dmi_handler(self.dbHandler, dmi_instr, log)
        else:
            self.dmi = None

    @pyqtSlot()
    def addToDatabase(self):
        self.log.logInfo(str(self.thread_id) + ": Running JSON Script...")
        time.sleep(1)

        try:
            if isinstance(self.script_s, str):
                self.__run_script(validate_json_script(self, self.script_s))

            elif isinstance(self.script_s, OrderedDict):
                for key, value in self.script_s.items():
                    if key[:1] != "__" and key[-2:] != "__":
                        self.__run_script(validate_json_script(self,value.get_script()))
                        self.done.emit(value.get_title())

        except json.decoder.JSONDecodeError as err:
            err_msg = "Failed Sending Document(s) To Database.\nBuild Interrupted With Error:\n" + str(err)
            self.update.emit(err_msg)
            self.log.logError(err_msg)
            self.thrd_done.emit(str(self.thread_id) + ": Run failed. See log for details.")
            return False
        self.thrd_done.emit(str(self.thread_id) + ": Run Complete.")
        time.sleep(1)

    def __run_script(self, script):
        data = script

        i = 0
        while i < len(data):
            self.start.emit(len(data))
            if self.stopFlag:
                return
            elif not self.pauseFlag:
                send_data = data[i]
                if self.dmi:
                    send_data = self.dmi.manipulate(data[i])
                self.dbHandler.insertDoc(send_data)
                self.update.emit("Sending Objects to Database... %d/%d" %(i+1, len(data)))
                time.sleep(1)
                i += 1
            else:
                continue
        return True

    def setStopFlag(self):
        self.log.logInfo(str(self.thread_id) + ": Run Terminated Before Completion")
        self.thrd_done.emit(str(self.thread_id) + ": Run Terminated Before Completion")
        self.stopFlag = True

    def togglePauseFlag(self):
        self.pauseFlag = not self.pauseFlag
  