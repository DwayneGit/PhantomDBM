from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolBar

class PhtmToolBar(QToolBar):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style = style
        self.set_style()
        self.setContextMenuPolicy(Qt.PreventContextMenu)

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QToolBar {
                    border-width: 0px;
                    background-color: rgb(46, 51, 58);
                }
                QToolButton {
                    border-width: 0px;
                    background-color: rgb(46, 51, 58);
                }
            """)
            