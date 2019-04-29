from PyQt5.QtWidgets import QComboBox

class PhtmComboBox(QComboBox):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style = style