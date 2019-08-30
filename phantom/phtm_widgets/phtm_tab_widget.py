import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTabWidget, QMessageBox

from phantom.utility import validateJsonScript

from phantom.phtmWidgets import PhtmPlainTextEdit, PhtmMessageBox

from phantom.applicationSettings import settings

class PhtmTabWidget(QTabWidget):
    clearTabsRequested = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.setMovable(True)
        self.setTabsClosable(True)
        self.hide()

        self.default_tab_count = 1
        self.tab_data = {}
        self.script_set = {}
        self.tabCloseRequested.connect(self.closeTab)

    def tabByText(self, text):
        tab_index_found = -1
        for i in range(self.count()):
            if text == self.tabText(i):
                tab_index_found = i
                self.setCurrentIndex(i)
                break
        return tab_index_found

    def saveEditor(self, index):
        if not self.widget(index).isChanged:
            return

        save_msg = "The current script is not saved. Do you want to save?"
        msg_box = PhtmMessageBox(self, "Save", save_msg, [QMessageBox.Yes, QMessageBox.Cancel])
        if msg_box.exec_():
            if msg_box.msg_selection == QMessageBox.Cancel:
                return False
            elif msg_box.msg_selection == QMessageBox.Yes:
                if self.widget(index).save_script():
                    self.is_saved(self.tabText(index), index)
                    return False

        return True

    def closeTab(self, index):
        if self.widget(index).isChanged:
            if not self.saveEditor(index):
                return

        self.removeTab(index)
        if self.count() < 1:
            self.hide()

    def clear(self):
        for index in range(self.count()):
            self.tabCloseRequested.emit(0)

    def addEditor(self, script=None):
        if script:
            editor = _PhtmEditor(script)
            editor.showLineNumbers()

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
        self.widget(index).isChanged = False
        self.setTabText(index, title)

        self.widget(index).get_treeItem().setText(0, title)

    def isChanged(self, index):
        if not self.widget(index).isChanged and self.tabText(index):
            self.widget(index).isChanged = True
            self.setTabText(index, "* " + self.tabText(index))

            self.widget(index).get_treeItem().setText(0, self.tabText(index))

    def get_index(self, editor):
        return self.indexOf(editor)

    def get_tab_text(self, index):
        if self.tabText(index)[0:2] == "* ":
            return self.tabText(index)[2:]
        else: return self.tabText(index)

class _PhtmEditor(PhtmPlainTextEdit):

    saved = pyqtSignal(str)

    def __init__(self, script=None):
        super(_PhtmEditor, self).__init__()

        self.filePath = None
        self.isChanged = False
        self.treeItem = None

        self.__currScript = script
        self.title = self.__currScript.getTitle()
        self.setPlainText(self.__currScript.getScript())

    def set_currScript(self, script):
        self.__currScript = script
        self.title = self.__currScript.getTitle()
        self.setPlainText(self.__currScript.getScript())
        self.isChanged = False

    def getCurrScript(self):
        return self.__currScript

    def save_script(self, user="Daru"):
        try:
            validateJsonScript(self, self.toPlainText())
        except Exception as err:
            error_msg = PhtmMessageBox(self, "Validation Error", "Invalid JSON:\n" + str(err))
            error_msg.exec_()
            return False

        self.__currScript.set_script(self.toPlainText())
        self.__currScript.set_modified_by(user)
        self.__currScript.update_date_time_modified()

        self.isChanged = False

        self.saved.emit(self.__currScript.getTitle())
        return True

    def get_treeItem(self):
        return self.treeItem

    def setTreeItem(self, item):
        self.treeItem = item