import re

from PyQt5.QtGui import QPainter, QColor, QTextFormat
from PyQt5.QtCore import QSize, pyqtSignal, QRect, Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QTabWidget, QMessageBox

from phantom.phtm_widgets import PhtmPlainTextEdit

class PhtmTabWidget(QTabWidget):
    clearTabsRequested = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.default_tab_count = 1
        self.tab_data = {}
        self.script_set = {}
        self.tabCloseRequested.connect(self.close_tab)

    def tab_by_text(self, text):
        tab_index_found = -1
        for i in range(self.count()):
            if text == self.tabText(i):
                tab_index_found = i
                self.setCurrentIndex(i)
                break
        return tab_index_found

    def close_tab(self, index):
        if self.widget(index).is_changed:
            save_msg = "The current script is not saved. Are you Sure you want to close?"
            reply = QMessageBox.question(self, 'Message', 
                            save_msg, QMessageBox.Yes | QMessageBox.Save | QMessageBox.Cancel, QMessageBox.Cancel)

            if reply == QMessageBox.Cancel:
                return
            elif reply == QMessageBox.Save:
                self.widget(index).save_script()
            elif reply == QMessageBox.Yes:
                self.is_saved(self.tabText(index)[2:], index)
                
        self.removeTab(index)
        if self.count() < 1:
            self.hide()

    def clear(self):
        for index in range(self.count()):
            self.tabCloseRequested.emit(0)

    def add_editor(self, script=None):
        if script:
            editor = _PhtmEditor(script)

            index = self.addTab(editor, editor.title)

            editor.textChanged.connect(lambda: self.isChanged(self.currentIndex()))
            editor.saved.connect(lambda title: self.is_saved(title, self.currentIndex()))

        else:
            editor = _PhtmEditor()
            index = self.addTab(editor, "")
            editor.textChanged.connect(lambda: self.isChanged(self.currentIndex()))
            editor.saved.connect(lambda title: self.is_saved(title, self.currentIndex()))

        self.setCurrentIndex(index)
        return index

    def is_saved(self, title, index):
        self.widget(index).is_changed = False
        self.setTabText(index, title)

        self.widget(index).get_tree_item().setText(0, title)

    def isChanged(self, index):
        if not self.widget(index).is_changed and self.tabText(index):
            self.widget(index).is_changed = True
            self.setTabText(index, "* " + self.tabText(index))

            self.widget(index).get_tree_item().setText(0, self.tabText(index))

    def get_index(self, editor):
        return self.indexOf(editor)

    def get_tab_text(self, index):
        if self.tabText(index)[0:2] == "* ":
            return self.tabText(index)[2:]
        else: return self.tabText(index)

class _LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth, 0)

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)

class _PhtmEditor(PhtmPlainTextEdit):

    saved = pyqtSignal(str)

    def __init__(self, script=None):
        super(_PhtmEditor, self).__init__()

        self.lineNumberArea = _LineNumberArea(self)

        self.file_path = None
        self.is_changed = False
        self.tree_item = None

        self.__curr_script = script
        self.title = self.__curr_script.get_title()
        self.setPlainText(self.__curr_script.get_script())

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)

        self.lineNumberAreaWidth = (3 + self.fontMetrics().width('9') * 4) + 5

    def set_curr_script(self, script):
        self.__curr_script = script
        self.title = self.__curr_script.get_title()
        self.setPlainText(self.__curr_script.get_script())
        self.is_changed = False

    def get_curr_script(self):
        return self.__curr_script

    def save_script(self, user="Daru"):
        self.__curr_script.set_script(self.toPlainText())
        self.__curr_script.set_modified_by(user)
        self.__curr_script.update_date_time_modified()

        self.saved.emit(self.__curr_script.get_title())

    def get_tree_item(self):
        return self.tree_item

    def set_tree_item(self, item):
        self.tree_item = item

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
        script = ""
        for line in htmlText.splitlines():
            self.appendHtml(line)

    def set_file_path(self, path):
        self.file_path = path

        file_name = re.split('^(.+)\/([^\/]+)$', path)
        self.title = file_name[2]
