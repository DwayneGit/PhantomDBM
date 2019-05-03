from PyQt5.QtWidgets import QTreeWidget

class PhtmTreeWidget(QTreeWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent