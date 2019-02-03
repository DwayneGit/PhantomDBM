import os
import re
from datetime import datetime

from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class cleanTmpScripts(QThread):
    def __init__(self, log, length_days = 0):
        QObject.__init__(self)
        self.log = log
        self.length_days = length_days
        self.thread_id = int(QThread.currentThreadId())  # cast to int() is necessary


    def clean(self): 
        num_deleted = 0
        self.log.logInfo(str(self.thread_id) + ": Cleaning temporary scripts...")
        for file in os.listdir("tmp"):
            if file.endswith(".json"):
                dtime = re.match(r"(script\_)(\w+)\.(\w+)", file) # get time created from file name

                datetime_object = datetime.strptime(dtime.group(2), '%w%d%m%y_%H%M%S') #covert time to datetime object

                dist = datetime_object - datetime.now()
                # print(dist.total_seconds()/86400) # get the time file has existed totals seconds / seconds in a day

                if datetime_object.day > self.length_days:
                    os.remove("tmp/" + file) # if file is longer than a day remove it
                    self.log.logInfo(str(self.thread_id) + ": " + file + " has been deleted")
                    num_deleted += 1
                
        self.log.logInfo(str(self.thread_id) + ": " + str(num_deleted) + " files deleted")

        

    def run(self):
        self.clean()