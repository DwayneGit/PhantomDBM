import re

from PyQt5.QtCore import QSize, Qt, QRect, Qt
from PyQt5.QtGui import QFont, QFontMetrics,  QPainter, QColor, QTextFormat
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit, QScrollBar

from phantom.application_settings import settings

class PhtmPlainTextEdit(QPlainTextEdit):
    def __init__(self, text=""):
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

    def showLineNumbers(self):

        self.lineNumberArea = _LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)

        self.lineNumberAreaWidth = (3 + self.fontMetrics().width('9') * 4) + 5

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins((3 + self.fontMetrics().width('9') * 4) + 5, 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        try:
            cr = self.contentsRect()
            self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                        self.lineNumberAreaWidth, cr.height()))
        except:
            pass

    def lineNumberAreaPaintEvent(self, event):
        mypainter = QPainter(self.lineNumberArea)

        mypainter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                mypainter.setPen(Qt.black)
                mypainter.drawText(0, top, self.lineNumberArea.width(), height,
                Qt.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(settings.__THEME__["color_scheme"]["highlight"])

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def setHtml(self, htmlText):
        self.clear()
        script = ""
        for line in htmlText.splitlines():
            self.appendHtml(line)

    def set_file_path(self, path):
        self.file_path = path

        file_name = re.split('^(.+)\/([^\/]+)$', path)
        self.title = file_name[2]

class _LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth, 0)

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)