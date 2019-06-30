import os
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread

from Naked.toolshed.shell import execute_js

from phantom.application_settings import settings

class mongoose_thread(QObject):
    start = pyqtSignal(int) # signal data ready to be appended to th board
    done = pyqtSignal(str)

    def __init__(self, dbHandler):
        QObject.__init__(self)
        self.dbHandler = dbHandler

    def run(self):
        try:
            execute_js('./phantom/database/js/index.js',
                       arguments=self.dbHandler.get_uri() + " " + self.dbHandler.get_collection() + 'Schema')
            print(os.getpid())

        except Exception as err:
            settings.__LOG__.logError(str(err))
