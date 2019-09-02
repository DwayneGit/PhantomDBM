import os
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread

from Naked.toolshed.shell import execute_js

from Phantom.ApplicationSettings import Settings

class MongooseThread(QObject):
    start = pyqtSignal(int) # signal data ready to be appended to th board
    done = pyqtSignal(str)

    def __init__(self, databaseHandler):
        QObject.__init__(self)
        self.databaseHandler = databaseHandler

    def insertDocs(self):
        try:
            execute_js('./Phantom/Database/js/index.js',
                       arguments="insert " + self.databaseHandler.getUri() + " " + self.databaseHandler.getCollection())
            print(os.getpid())

        except Exception as err:
            Settings.__LOG__.logError(str(err))


    def find_docs(self):
        try:
            execute_js('./Phantom/Database/js/index.js',
                       arguments="find " + self.databaseHandler.getUri() + " " + self.databaseHandler.getCollection() + 'Schema')
            print(os.getpid())

        except Exception as err:
            Settings.__LOG__.logError(str(err))
