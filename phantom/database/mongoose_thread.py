import os
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread

from Naked.toolshed.shell import executeJScript

from phantom.applicationSettings import settings

class mongoose_thread(QObject):
    start = pyqtSignal(int) # signal data ready to be appended to th board
    done = pyqtSignal(str)

    def __init__(self, databaseHandler):
        QObject.__init__(self)
        self.databaseHandler = databaseHandler

    def insertDocs(self):
        try:
            executeJScript('./phantom/database/js/index.js',
                       arguments="insert " + self.databaseHandler.getUri() + " " + self.databaseHandler.getCollection())
            print(os.getpid())

        except Exception as err:
            settings.__LOG__.logError(str(err))


    def find_docs(self):
        try:
            executeJScript('./phantom/database/js/index.js',
                       arguments="find " + self.databaseHandler.getUri() + " " + self.databaseHandler.getCollection() + 'Schema')
            print(os.getpid())

        except Exception as err:
            settings.__LOG__.logError(str(err))
