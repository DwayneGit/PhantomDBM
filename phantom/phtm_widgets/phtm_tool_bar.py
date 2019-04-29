from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolBar

class PhtmToolBar(QToolBar):
    def __init__(self, style="ghost"):
        super().__init__()
        self.setContextMenuPolicy(Qt.PreventContextMenu)
            