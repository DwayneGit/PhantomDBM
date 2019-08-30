
import os
import sys
import json
import time
import signal
import socket

from collections import OrderedDict

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread
from phantom.instructions import DmiHandler

from phantom.utility import validateJsonScript

from phantom.applicationSettings import settings

from Naked.toolshed.shell import executeJScript

class uploadScriptThread(QObject):
    updateStatus = pyqtSignal(str) # signal data ready to be appended to th board
    updateBoard = pyqtSignal(str) # signal data ready to be appended to th board
    start = pyqtSignal(int) # signal data ready to be appended to th board
    done = pyqtSignal(str)

    threadDone = pyqtSignal(str) # done signal

    def __init__(self, script_s, databaseHandler, dmiInstr=None):
        QObject.__init__(self)
        self.script_s = script_s
        self.databaseHandler = databaseHandler
        self.pauseFlag = False
        self.stopFlag = False

        self.threadId = int(QThread.currentThreadId())  # cast to int() is necessary

        if dmiInstr:
            self.dmi = DmiHandler(self.databaseHandler, dmiInstr)
        else:
            self.dmi = None

    @pyqtSlot()
    def addToDatabase(self):
        settings.__LOG__.logInfo(str(self.threadId) + ": Running JSON Script...")
        time.sleep(1)

        try:
            if isinstance(self.script_s, str):
                self.__runScript(validateJsonScript(self, self.script_s))

            elif isinstance(self.script_s, OrderedDict):
                for key, value in self.script_s.items():
                    if key[:1] != "__" and key[-2:] != "__":
                        self.__runScript(validateJsonScript(None, value.getScript()))
                        self.done.emit(value.getTitle())

        except json.decoder.JSONDecodeError as err:
            errorMessage = "UPLD_ERR: Failed Sending Document(s) To Database.\nBuild Interrupted With Error:\n" + str(err)
            self.updateBoard.emit(str(self.threadId) + ": UPLD_ERR: Failed Sending Document To Database.\nBuild Interrupted With Error:\n" + str(err))
            settings.__LOG__.logError("RUN_ERR:" + str(errorMessage))
            self.threadDone.emit(str(self.threadId) + ": Run failed. See log for details.")
            return False

        if not self.stopFlag:
            self.threadDone.emit(str(self.threadId) + ": Run Complete.")
        time.sleep(1)

    def __runScript(self, script):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        serverAddress = "./phantom/database/js/src/tmp/db.sock"
        settings.__LOG__.logInfo('Connecting to %s' % serverAddress)

        try:
            s.connect(serverAddress)

        except socket.error as err:
            settings.__LOG__.logError(str(err))
            self.threadDone.emit(str(self.threadId) + ": " + str(err))
            self.setStopFlag()

        if isinstance(script, dict):
            for model, docs in script.items():
                s.sendall(bytes("set_model", encoding='utf-8'))
                data = s.recv(1024)
                print(data.decode("utf-8"))
                time.sleep(1)
                s.sendall(bytes(model, encoding='utf-8'))
                data = s.recv(1024)
                print(data.decode("utf-8"))
                time.sleep(1)
                self.__docsToRun(s, docs)
        else:
            s.sendall(bytes("set_model", encoding='utf-8'))
            data = s.recv(1024)
            time.sleep(1)
            s.sendall(bytes(settings.__DATABASE__.getCollectionName(), encoding='utf-8'))
            time.sleep(1)
            self.__docsToRun(s, script)

        settings.__LOG__.logInfo('Client closing socket...')
        
        s.sendall(bytes("end", encoding='utf-8'))

        s.shutdown(1)
        s.close()

    def __docsToRun(self, s, docs):
        for i in range(0, len(docs)):
            self.start.emit(len(docs))
            if self.stopFlag:
                return
            elif not self.pauseFlag:
                sendData = docs[i]
                if self.dmi:
                    sendData = self.dmi.manipulate(docs[i])
                try:
                    s.sendall(bytes(json.dumps(sendData), encoding='utf-8'))
                    data = s.recv(1024)
                    if data.decode("utf-8") == "err":
                        raise Exception
                except Exception as err:
                    self.updateBoard.emit("Failed to upload document %d/%d" %(i+1, len(docs)) + "\n" + str(err))
                    continue
                finally:
                    # print(data.decode("utf-8") + str(i))
                    self.updateStatus.emit("Sending Objects to Database... %d/%d" %(i+1, len(docs)))
                    time.sleep(1)
            else:
                continue

        self.threadDone.emit(str(self.threadId) + ": Complete")

    def setStopFlag(self):
        settings.__LOG__.logInfo(str(self.threadId) + ": Run Terminated Before Completion")
        self.threadDone.emit(str(self.threadId) + ": Run Terminated Before Completion")
        self.stopFlag = True

    def togglePauseFlag(self):
        self.pauseFlag = not self.pauseFlag
  