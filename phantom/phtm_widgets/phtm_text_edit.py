from PyQt5.QtWidgets import QTextEdit

class PhtmTextEdit(QTextEdit):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style = style
        self.set_style()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QTextEdit {
                    background-color: rgb(46, 51, 58);
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    color: white;
                }
            """)