from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
import re

from style.phtm_plain_text_edit import phtm_plain_text_edit
from file.json_script import json_script

import text_style as text_style

import numpy as np

class LineNumberArea(QWidget):

    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth, 0)

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)


class phtm_editor(phtm_plain_text_edit):
    def __init__(self, script=None):
        super(phtm_editor, self).__init__()
        self.lineNumberArea = LineNumberArea(self)

        self.title = None
        self.file_path = None
        self.is_changed = False

        self.__curr_script = script

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)

        self.lineNumberAreaWidth = (3 + self.fontMetrics().width('9') * 4) + 5
    
    def set_curr_script(self, script):
        self.__curr_script = script

    def get_curr_script(self):
        return self.__curr_script

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

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                    self.lineNumberAreaWidth, cr.height()))

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

            lineColor = QColor(92, 0, 153).lighter(160)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def setHtml(self, htmlText):
        self.clear()
        self.appendHtml(htmlText)
        text_style.translate_text(htmlText, self)

    def set_file_path(self, path):
        self.file_path = path

        file_name = re.split('^(.+)\/([^\/]+)$', path)
        self.title = file_name[2]

    # def setTabTitle(self, index, title):
    #     # use regex to grab the name of the file from the path and added to title
    #     newTitle = self.parent.progTitle
    #     newTitle = self.tabText(index) + " - " + newTitle
    #     self.parent.set_window_title(newTitle)
    #     self.parent.currTitle = newTitle
    #     print(newTitle)
