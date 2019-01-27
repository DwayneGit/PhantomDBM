import sys
import os
import json
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 

class Pause(QObject):

    pause = pyqtSignal(str)

    @pyqtSlot()
    def pauseThread(self):
