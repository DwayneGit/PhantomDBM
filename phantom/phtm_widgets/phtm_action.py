from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QAction

class PhtmAction(QAction):
    def __init__(self, signal, icon=None, text=None, parent=None):
        super().__init__(QIcon(icon()), text, parent)
        signal.connect(lambda: self.change_Icon(icon))

    @pyqtSlot()
    def change_Icon(self, icon):
        self.setIcon(QIcon(icon()))
