import sys

from PyQt5.QtWidgets import QApplication

from phantom import PhtmMainWindow

import os
try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
except KeyError as err:
    print(str(err))
    user_paths = []

print( user_paths)

if __name__ == '__main__':
    APP = QApplication(sys.argv)

    MANAGER = PhtmMainWindow()

    MANAGER.show()
    sys.exit(APP.exec_())
