import sys
import os
import json

from PyQt5.QtWidgets import QApplication

from phantom import PhtmMainWindow, settings

if __name__ == '__main__':
    settings.init("phantom/application_settings/app_settings.json")

    APP = QApplication(sys.argv)
    APP.setStyleSheet(settings.__STYLESHEET__)

    MANAGER = PhtmMainWindow()

    MANAGER.show()
    sys.exit(APP.exec_())
