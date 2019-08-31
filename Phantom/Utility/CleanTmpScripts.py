import os
import re

from datetime import datetime

from PyQt5.QtCore import QObject, QThread
from Phantom.ApplicationSettings import Settings

class CleanTmpScripts(QThread):
    def __init__(self, length_days=0):
        QObject.__init__(self)
        
        self.length_days = length_days
        self.threadId = int(QThread.currentThreadId())  # cast to int() is necessary


    def clean(self):
        num_deleted = 0
        Settings.__LOG__.logInfo(str(self.threadId) + ": Cleaning temporary scripts...")

        if not os.path.isdir('./tmp'):
            os.mkdir("tmp") # create folder fo temporary scripts

        for file in os.listdir("tmp"):
            if file.endswith(".json"):
                dtime = re.match(r"(script\_)(\w+)\.(\w+)", file) # get time created from file name

                datetime_object = datetime.strptime(dtime.group(2), '%w%d%m%y_%H%M%S') #covert time to datetime object

                # dist = datetime_object - datetime.now()
                # print(dist.total_seconds()/86400) # get the time file has existed totals seconds / seconds in a day

                if datetime_object.day > self.length_days:
                    os.remove("tmp/" + file) # if file is longer than a day remove it
                    Settings.__LOG__.logInfo(str(self.threadId) + ": " + file + " has been deleted")
                    num_deleted += 1

        Settings.__LOG__.logInfo(str(self.threadId) + ": " + str(num_deleted) + " files deleted")

    def run(self):
        self.clean()
