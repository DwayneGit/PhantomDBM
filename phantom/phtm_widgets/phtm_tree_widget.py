from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView
from PyQt5.QtCore import Qt

class PhtmTreeWidget(QTreeWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setColumnCount(1)
        self.setContentsMargins(0, 50, 0, 0)
        self.setHeaderHidden(True)

        self.setHeaderLabels(["Script Cluster"])

        self.setContextMenuPolicy(Qt.CustomContextMenu)
