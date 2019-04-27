from PyQt5.QtWidgets import QComboBox

class phtm_combo_box(QComboBox):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style=style
        self.set_style()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QComboBox {
                    background-color: rgb(46, 51, 58);
                    color: rgb(217, 217, 217);
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    font: bold 14px;
                    min-width: 10em;
                    padding: 6px;
                }
                QComboBox::drop-down{
                    border-style: outset;
                    border-width: 0px;
                    border-color: rgb(39, 44, 51);
                    color: rgb(46, 51, 58);
                    padding: 0px;
                }
                QComboBox::item{
                    background-color: rgb(46, 51, 58);
                    color: rgb(217, 217, 217);
                }
                QComboBox::item::selected{
                    background-color: rgb(39, 44, 51);
                }
            """)