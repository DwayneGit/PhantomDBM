import sys
import os
import json
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 

class Thread1(QObject):

    update = pyqtSignal(str)
    done = pyqtSignal(int)

    def __init__(self, filePath, dbHandler):
        QObject.__init__(self)
        self.filePath = filePath
        self.dbHandler = dbHandler

    @pyqtSlot()
    def addToDatabase(self):

        # thread_name = QThread.currentThread().objectName()
        thread_id = int(QThread.currentThreadId())  # cast to int() is necessary

        # print("Opening Child FIFO...")
        self.update.emit("Running JSON Script...")
        time.sleep(1)
                        
        with open(self.filePath) as infile:
            data = json.load(infile)
            for i in range(len(data)):
                self.dbHandler.insertDoc(data[i])
                self.update.emit("Sending Objects to Database... %d/%d" %(i+1,len(data)))
                time.sleep(1)
                # print(1)

        # self.update.emit("Finished")
        self.done.emit(thread_id)
        time.sleep(1)
 
    # def updateSignal(self, msg):
    #     self.update.emit(msg)
        

# class Thread2(QThread):

#     def __init__(self):
#         QThread.__init__(self)

#     def __del__(self):
#         print("Opening Parent FIFO...")
#         with open(FIFO) as fifo:
#             print("Parent FIFO Opened.")
#             while True:
#                 # print(2)
#                 message = fifo.readline()
#                 self.update.emit(message)
#                 print(message)

#                 if len(message) == 0:
#                     print("Writer closed")
#                     break

#         fifo.close()
#         sys.exit()

#     def run(self):
#         # your logic here       