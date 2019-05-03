from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class phtm_plain_text_edit(QPlainTextEdit):
    def __init__(self, style="ghost"):
        super().__init__()
        self.style=style

        self.scroll_bar = QScrollBar()
        self.addScrollBarWidget(self.scroll_bar, Qt.AlignRight)

        self.set_style()

    def set_style(self):
        if self.style == "ghost":
            self.setStyleSheet("""
                QPlainTextEdit {
                    background-color: rgb(46, 51, 58);
                    border-style: outset;
                    border-width: 1px;
                    border-color: rgb(39, 44, 51);
                    color: white;
                }
            """)
            self.scroll_bar.setStyleSheet("""
                QScrollBar:vertical {
                    width: 10px;
                    background: rgb(46, 51, 58);
                }

                QScrollBar::handle:vertical {
                    min-height: 5px;
                }

                QScrollBar::add-line:vertical {
                    background: none;
                    height: 45px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }

                QScrollBar::sub-line:vertical {
                    background: none;
                    height: 45px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }               

                QScrollBar::up-arrow:vertical { 
                    height: 3px; 
                    width: 3px 
                }

                QScrollBar::down-arrow:vertical {
                    height: 3px; 
                    width: 3px 
                }                   
                
            """)