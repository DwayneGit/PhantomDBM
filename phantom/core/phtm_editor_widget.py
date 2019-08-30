import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPlainTextEdit, QSplitter, QHBoxLayout, QWidget, QVBoxLayout, QAbstractItemView, QMenu, QAction, QTreeWidgetItem

import phantom.utility.textStyle as textStyle
from phantom.phtmWidgets import PhtmTreeWidget, PhtmPlainTextEdit, PhtmTabWidget
from phantom.file_stuff import PhmFileHandler

from phantom.applicationSettings import settings

class PhtmEditorWidget(QWidget):
    def __init__(self, fileHandler , parent=None):
        super().__init__()
        self.parent = parent
        self.__cluster = PhmFileHandler()

        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)

        self.__splitter = QSplitter()

        self.__editorTabs = PhtmTabWidget(self)
        self.__editorTabs.currentChanged.connect(self.tabChanged)

        self.__splitter.addWidget(self.__editorTabs)

        self.__initScriptTree()

        self.__defaultCount = 0

        self.fileHandler  = fileHandler 

        self.nameTemp = None

        self.__splitter.setSizes([200, 150])
        self.__layout.addWidget(self.__splitter)

        self.setLayout(self.__layout)

    def tabChanged(self, index):
        scriptName = self.__editorTabs.tabText(index)
        for i in range(self.__treeRoot.childCount()):
            if self.__treeRoot.child(i).text(0) == scriptName:
                self.__scriptTree.setCurrentItem(self.__treeRoot.child(i))
                break

    def clearTabs(self):
        self.__editorTabs.clear()

    def __openScript(self, item):
        if item == self.__treeRoot or (self.__editorTabs.tabByText(item.text(0)) != -1):
            return

        if self.__editorTabs.isHidden():
            self.__editorTabs.show()
            self.__editorTabs.addEditor(self.__cluster.getPhmScripts()[item.text(0)])

            self.__editorTabs.currentWidget().textChanged.disconnect()
            self.__editorTabs.currentWidget().setTreeItem(item)

            self.__editorTabs.setTabText(self.__editorTabs.currentIndex(), item.text(0))
            self.__editorTabs.currentWidget().isChanged = False

            self.__editorTabs.currentWidget().textChanged.connect(lambda: self.__editorTabs.isChanged(self.__editorTabs.currentIndex()))

        elif self.__editorTabs.currentWidget().isChanged:
            self.__openScriptInTab(item)

        else:
            self.__editorTabs.currentWidget().textChanged.disconnect()
            
            self.__editorTabs.currentWidget().setCurrScript(self.__cluster.getPhmScripts()[item.text(0)])
            self.__editorTabs.currentWidget().setTreeItem(item)

            self.__editorTabs.setTabText(self.__editorTabs.currentIndex(), item.text(0))

            self.__editorTabs.currentWidget().textChanged.connect(lambda: self.__editorTabs.isChanged(self.__editorTabs.currentIndex()))

    def __openScriptInTab(self, treeItem):
        index = self.__editorTabs.addEditor(self.__cluster.getPhmScripts()[treeItem.text(0)])
        self.__editorTabs.widget(index).setTreeItem(treeItem)

    def loadCluster(self, filePath, filename):
        self.__cluster.load(filePath)

        self.__scriptTree.itemSelectionChanged.disconnect()
        self.__scriptTree.clear()
        self.__scriptTree.itemSelectionChanged.connect(lambda: self.__showDetails(self.__scriptTree.currentItem()))

        self.__treeRoot = self.addScriptRoot()
        self.__scriptTree.expandItem(self.__treeRoot)

        self.__editorTabs.hide()

        for key, value in self.__cluster.getPhmScripts().items():
            if key[:1] != "__" and key[-2:] != "__":
                self.addScriptChild(self.__treeRoot, value.getTitle())

    def __createNewScript(self, item, col):
        try:
            newScript = self.__cluster.addScript("[\n    {\n        \"\": \"\"\n    }\n]", item.text(col), "Default")
        except Exception as err:
            settings.__LOG__.logError("EDIT_WIDG_ERR:" + str(err))
            return

        if self.__editorTabs.isHidden():
            self.__editorTabs.show()

        index = self.__editorTabs.addEditor(newScript)
        self.__editorTabs.widget(index).setTreeItem(item)

    def addNewScript(self):
        item = self.addScriptChild(self.__treeRoot, "")

        self.__scriptTree.setCurrentItem(item)
        self.__scriptTree.editItem(item)

    def loadScript(self):
        fileName, filePath = self.fileHandler.loadScript()
        try:
            newScript = self.__cluster.addScript(textStyle.readText(filePath), fileName, "Dwayne W")
        except Exception as err:
            settings.__LOG__.logError("EDIT_WIDG_ERR: " + str(err))
            return

        item = self.addScriptChild(self.__treeRoot, fileName)

        if self.__editorTabs.isHidden():
            self.__editorTabs.show()

        index = self.__editorTabs.addEditor(newScript)
        self.__editorTabs.widget(index).setTreeItem(item)

        return newScript, item

    def __initScriptTree(self):
        self.__treeRoot = None

        self.__scriptTree = PhtmTreeWidget()

        self.__scriptTree.itemDelegate().closeEditor.connect(self.__editorClosed)

        self.__scriptTreeDetailsBox = PhtmPlainTextEdit()
        self.__scriptTreeDetailsBox.setReadOnly(True)
        self.__scriptTreeDetailsBox.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        self.__scriptTreeLayout = QVBoxLayout()
        self.__scriptTreeLayout.addWidget(self.__scriptTree)
        self.__scriptTreeLayout.addWidget(self.__scriptTreeDetailsBox)
        self.__scriptTreeLayout.setContentsMargins(0, 26, 0, 0)

        self.__scriptTreeWidget = QWidget()
        self.__scriptTreeWidget.setLayout(self.__scriptTreeLayout)

        self.__scriptTree.itemDoubleClicked.connect(self.__openScript)
        self.__scriptTree.itemSelectionChanged.connect(lambda: self.__showDetails(self.__scriptTree.currentItem()))

        self.__treeRoot = self.addScriptRoot()
        self.__scriptTree.setCurrentItem(self.__treeRoot)
        self.__scriptTree.expandItem(self.__treeRoot)
        self.__scriptTree.customContextMenuRequested.connect(self.handleContextMenuRequested)

        self.__splitter.addWidget(self.__scriptTreeWidget)

    def __editorClosed(self, editor, hint):
        item = self.__scriptTree.currentItem()
        if editor.text() and not editor.text().isspace():
            if not self.nameTemp:
                self.__createNewScript(item, 0)
                return

            if item == self.__treeRoot:
                self.__cluster.getPhm().setName(editor.text())
                self.nameTemp = None
                return

            if not item.text(0):
                item.setText(0, self.nameTemp)

            self.__cluster.getPhmScripts()[item.text(0)] = self.__cluster.getPhmScripts()[self.nameTemp]
            self.__cluster.getPhmScripts()[item.text(0)].setTitle(item.text(0))
            del self.__cluster.getPhmScripts()[self.nameTemp]

            i = self.__editorTabs.tabByText(self.nameTemp)
            if i != -1:
                self.__editorTabs.setTabText(i, item.text(0))

        elif self.nameTemp:
            item.setText(0, self.nameTemp)
        else:
            self.__treeRoot.removeChild(item)

        self.nameTemp = None

    def __showDetails(self, item):
        if not item or not item.text(0):
            return

        if item != self.__treeRoot:
            txt = item.text(0)
            if item.text(0)[0:2] == "* ":
                txt = item.text(0)[2:]
    
            currScirpt = self.__cluster.getPhmScripts()[txt]

            details = "Title: " + currScirpt.getTitle()
            details += "\nDate Created: " +  str(currScirpt.getDateTimeCreated())
            details += "\nDate Modified: " + str(currScirpt.getDateTimeModified())
            details += "\nCreated By: " + currScirpt.getCreator()
            details += "\nLast Modified By: " + currScirpt.getModifiedBy()

        else:
            details = "Title: " + item.text(0)
            details += "\nFile Path: " + self.__cluster.getFilePath()

        self.__scriptTreeDetailsBox.setPlainText(details)

    def deleteScript(self, index):
        item = self.__treeRoot.child(index)
        self.__editorTabs.closeTab(self.__editorTabs.tabByText(item.text(0)))
        del self.__cluster.getPhmScripts()[item.text(0)]
        self.__treeRoot.removeChild(item)

    def renameScript(self, index):
        item = self.__treeRoot.child(index)
        self.__scriptTree.editItem(item)
        self.nameTemp = item.text(0)

    def handleContextMenuRequested(self, pos):
        item = self.__scriptTree.itemAt(pos)
        self.__scriptTree.itemClicked.emit(item, 0)
        if item:
            menu = QMenu(self)
            if self.__scriptTree.indexOfTopLevelItem(item) == -1:

                index = item.parent().indexOfChild(item)
                renameAction = QAction("Rename", self)
                renameAction.triggered.connect(lambda x: self.renameScript(index))

                deleteAction = QAction("Delete", self)
                deleteAction.triggered.connect(lambda x: self.deleteScript(index))

                menu.addAction(renameAction)
                menu.addAction(deleteAction)

                menu.addSeparator()

                openAction = QAction("Open", self)
                openAction.triggered.connect(lambda x: self.__openScript(self.__scriptTree.selectedItems()[0]))

                openTabAction = QAction("Open In New Tab", self)
                openTabAction.triggered.connect(lambda x: self.__openScriptInTab(self.__scriptTree.selectedItems()[0]))

                menu.addAction(openAction)
                menu.addAction(openTabAction)

                menu.addSeparator()

                runAction = QAction("Run", self)
                runAction.triggered.connect(lambda: self.parent.r_ctrl.run(0))

                runBelow = QAction("Run + Scripts Below", self)
                runBelow.triggered.connect(lambda: self.parent.r_ctrl.run(2, index))

                menu.addAction(runAction)
                menu.addAction(runBelow)

            else:
                newAction = QAction("Rename Cluster", self)
                newAction.triggered.connect(lambda x: self.renameScriptRoot())
                menu.addAction(newAction)

                newAction = QAction("New Script", self)
                newAction.triggered.connect(lambda x: self.addNewScript())
                menu.addAction(newAction)

                menu.addSeparator()

                runAllAction = QAction("Run All", self)
                runAllAction.triggered.connect(lambda: self.parent.r_ctrl.run(1))
                menu.addAction(runAllAction)

            menu.popup(self.__scriptTree.viewport().mapToGlobal(pos))

    def renameScriptRoot(self, name=None):
        if not name:
            self.nameTemp = self.__treeRoot.text(0)
            self.__scriptTree.editItem(self.__treeRoot)
        self.__treeRoot.setText(0, name)

    def addScriptRoot(self):
        treeItem = QTreeWidgetItem(self.__scriptTree)
        treeItem.setText(0, self.__cluster.getPhm().getName())
        treeItem.setFlags(treeItem.flags() | Qt.ItemIsEditable)
        treeItem.setIcon(0, QIcon(settings.__ICONS__.whiteDot))
        return treeItem

    def addScriptChild(self, root, name):
        treeItem = QTreeWidgetItem(root)
        treeItem.setText(0, name)
        treeItem.setFlags(treeItem.flags() | Qt.ItemIsEditable)
        root.addChild(treeItem)
        return treeItem

    def getScriptTree(self):
        return self.__scriptTree

    def getEditorTabs(self):
        return self.__editorTabs

    def getCluster(self):
        return self.__cluster

    def savePhm(self, filePath):
        self.parent.body.statusBar().showMessage("Saving PHM ...")
        for i in range(self.__editorTabs.count()):
            self.__editorTabs.saveEditor(i)

        self.__cluster.save(filePath)

        filenameWithExtension = os.path.basename(filePath)
        filename = os.path.splitext(filenameWithExtension)[0]

        if self.__treeRoot.text(0) == "New Cluster":
            self.renameScriptRoot(filename)
            self.parent.updateWindowTitle(filename)
