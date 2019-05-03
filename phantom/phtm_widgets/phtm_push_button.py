from PyQt5.QtWidgets import QPushButton

class PhtmPushButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFlat(True)