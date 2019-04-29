from PyQt5.QtWidgets import QTextEdit

class PhtmTextEdit(QTextEdit):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style = style