import sys
import os
import json

from PyQt5.QtWidgets import QApplication

from Phantom import MainWindow, Settings

if __name__ == '__main__':
    APP = QApplication(sys.argv)

    Settings.init(APP, "Phantom/ApplicationSettings/app_settings.json")
    APP.setStyleSheet(Settings.__STYLESHEET__)

    MANAGER = MainWindow()
    MANAGER.show()
    sys.exit(APP.exec_())
