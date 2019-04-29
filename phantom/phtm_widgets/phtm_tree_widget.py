from PyQt5.QtWidgets import QTreeWidget

class PhtmTreeWidget(QTreeWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.set_style()

    def set_style(self):
        self.setStyleSheet('''
            QTreeWidget {
                background-color: rgb(46, 51, 58);
                border-style: outset;
                border-width: 1px;
                border-color: rgb(39, 44, 51);
                color: rgb(217, 217, 217);
            }

            QHeaderView::section {
                background-color: rgb(46, 51, 58);
                color: rgb(217, 217, 217);
                padding-left: 4px;
                border: none;
            }

        ''')
