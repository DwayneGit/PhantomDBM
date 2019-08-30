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

        self.defaultTabCount = 1
        self.tabData = {}
        self.scriptSet = {}
        self.tabCloseRequested.connect(self.closeTab)

    def tabByText(self, text):
        tabIndexFound = -1
        for i in range(self.count()):
            if text == self.tabText(i):
                tabIndexFound = i
                self.setCurrentIndex(i)
                break
        return tabIndexFound

    def saveEditor(self, index):
        if not self.widget(index).isChanged:
            return

        saveMessage = "The current script is not saved. Do you want to save?"
        messageBox = PhtmMessageBox(self, "Save", saveMessage, [QMessageBox.Yes, QMessageBox.Cancel])
        if messageBox.exec_():
            if messageBox.messageSelection == QMessageBox.Cancel:
                return False
            elif messageBox.messageSelection == QMessageBox.Yes:
                if self.widget(index).saveScript():
                    self.isSaved(self.tabText(index), index)
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
            editor.saved.connect(lambda title: self.isSaved(title, self.currentIndex()))

        else:
            editor = _PhtmEditor()
            index = self.addTab(editor, "")
            editor.textChanged.connect(lambda: self.isChanged(self.currentIndex()))
            editor.saved.connect(lambda title: self.isSaved(title, self.currentIndex()))

        self.setCurrentIndex(index)
        return index

    def isSaved(self, title, index):
        self.widget(index).isChanged = False
        self.setTabText(index, title)

        self.widget(index).getTreeItem().setText(0, title)

    def isChanged(self, index):
        if not self.widget(index).isChanged and self.tabText(index):
            self.widget(index).isChanged = True
            self.setTabText(index, "* " + self.tabText(index))

            self.widget(index).getTreeItem().setText(0, self.tabText(index))

    def getIndex(self, editor):
        return self.indexOf(editor)

    def getTabText(self, index):
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

    def setCurrScript(self, script):
        self.__currScript = script
        self.title = self.__currScript.getTitle()
        self.setPlainText(self.__currScript.getScript())
        self.isChanged = False

    def getCurrScript(self):
        return self.__currScript

    def saveScript(self, user="Daru"):
        try:
            validateJsonScript(self, self.toPlainText())
        except Exception as err:
            errorMessage = PhtmMessageBox(self, "Validation Error", "Invalid JSON:\n" + str(err))
            errorMessage.exec_()
            return False

        self.__currScript.setScript(self.toPlainText())
        self.__currScript.setModifiedBy(user)
        self.__currScript.updateDateTimeModified()

        self.isChanged = False

        self.saved.emit(self.__currScript.getTitle())
        return True

    def getTreeItem(self):
        return self.treeItem

    def setTreeItem(self, item):
        self.treeItem = item