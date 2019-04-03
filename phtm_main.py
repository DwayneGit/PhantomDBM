import os
import re
import sys

from PyQt5.QtWidgets import QApplication

from main_window import main_window
from phtm_widgets.phtm_main_window import phtm_main_window

if __name__ == '__main__':
    
    APP = QApplication(sys.argv)

    MANAGER = phtm_main_window()
    MANAGER.setCentralWidget(main_window(MANAGER))

    MANAGER.show()
    sys.exit(APP.exec_())

