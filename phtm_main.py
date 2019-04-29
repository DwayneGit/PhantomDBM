import sys
import os

from PyQt5.QtWidgets import QApplication

from phantom import PhtmMainWindow, settings

if __name__ == '__main__':
    settings.init()

    APP = QApplication(sys.argv)
    APP.setStyleSheet(settings.__THEME__)

    MANAGER = PhtmMainWindow()

    MANAGER.show()
    sys.exit(APP.exec_())
