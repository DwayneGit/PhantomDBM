from PyQt5.QtWidgets import QPushButton

class phtm_push_button(QPushButton):
    def __init__(self, text, parent=None, style="ghost"):
        super().__init__(text, parent)
        self.setFlat(True)
        self.style=style
        self.set_style()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgb(46, 51, 58);
                    color: rgb(217, 217, 217);
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    font: bold 14px;
                    padding: 6px;
                }
                QPushButton:pressed {
                    background-color: rgb(39, 44, 51);
                    border-style: inset;
                }
            """)