from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QPlainTextEdit, QScrollBar

__all__ = ['PhtmPlainTextEdit']

class PhtmPlainTextEdit(QPlainTextEdit):
    def __init__(self, text=None):
        super().__init__()

        font = QFont()
        font.setFamily("Courier")
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(10)

        self.setFont(font)
        tabStop = 4

        metrics = QFontMetrics(font)
        self.setTabStopWidth(tabStop * metrics.width(' '))

        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.setPlainText(text)

    def appendPlainText(self, text):
        self.setPlainText(self.toPlainText() + "\n" + text)