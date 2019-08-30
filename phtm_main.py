import sys
import os
import json

from PyQt5.QtWidgets import QApplication

from phantom import MainWindow, settings

if __name__ == '__main__':
    APP = QApplication(sys.argv)

    settings.init(APP, "phantom/application_settings/app_settings.json")
    APP.setStyleSheet(settings.__STYLESHEET__)

    MANAGER = MainWindow()

    MANAGER.show()
    sys.exit(APP.exec_())
