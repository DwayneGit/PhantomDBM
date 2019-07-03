import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPlainTextEdit, QSplitter, QHBoxLayout, QWidget, QVBoxLayout, QAbstractItemView, QMenu, QAction, QTreeWidgetItem

import phantom.utility.text_style as text_style
from phantom.phtm_widgets import PhtmTreeWidget, PhtmPlainTextEdit, PhtmTabWidget
from phantom.file_stuff import load_script, PhmFileHandler

from phantom.application_settings import settings

class PhtmEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.__cluster = PhmFileHandler()

        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)

        self.__splitter = QSplitter()

        self.__init_editor()
        self.__init_script_tree()

        self.__default_count = 0

        self.name_temp = None

        self.__splitter.setSizes([200, 150])
        self.__layout.addWidget(self.__splitter)

        self.setLayout(self.__layout)

    def __init_editor(self):
        self.__editor_tabs = PhtmTabWidget(self)

        self.__editor_tabs.setMovable(True)
        self.__editor_tabs.setTabsClosable(True)

        self.__splitter.addWidget(self.__editor_tabs)
        self.__editor_tabs.hide()

        self.__editor_tabs.currentChanged.connect(self.tab_changed)

    def tab_changed(self, index):
        scrpt = self.__editor_tabs.tabText(index)

        for i in range(self.__tree_root.childCount()):
            if self.__tree_root.child(i).text(0) == scrpt:
                self.__script_tree.setCurrentItem(self.__tree_root.child(i))

    def clear_tabs(self):
        self.__editor_tabs.clear()

    def __open_script(self, item):
        if item == self.__tree_root or (self.__editor_tabs.tab_by_text(item.text(0)) != -1):
            return

        if self.__editor_tabs.isHidden():
            self.__editor_tabs.show()
            self.__editor_tabs.add_editor(self.__cluster.get_phm_scripts()[item.text(0)])

            self.__editor_tabs.currentWidget().textChanged.disconnect()
            self.__editor_tabs.currentWidget().set_tree_item(item)

            self.__editor_tabs.setTabText(self.__editor_tabs.currentIndex(), item.text(0))
            self.__editor_tabs.currentWidget().is_changed = False

            self.__editor_tabs.currentWidget().textChanged.connect(lambda: self.__editor_tabs.isChanged(self.__editor_tabs.currentIndex()))

        elif self.__editor_tabs.currentWidget().is_changed:
            self.__open_script_in_tab(item)

        else:
            self.__editor_tabs.currentWidget().textChanged.disconnect()
            
            self.__editor_tabs.currentWidget().set_curr_script(self.__cluster.get_phm_scripts()[item.text(0)])
            self.__editor_tabs.currentWidget().set_tree_item(item)

            self.__editor_tabs.setTabText(self.__editor_tabs.currentIndex(), item.text(0))

            self.__editor_tabs.currentWidget().textChanged.connect(lambda: self.__editor_tabs.isChanged(self.__editor_tabs.currentIndex()))


    def __open_script_in_tab(self, tree_item):
        index = self.__editor_tabs.add_editor(self.__cluster.get_phm_scripts()[tree_item.text(0)])
        self.__editor_tabs.widget(index).set_tree_item(tree_item)

    def load_cluster(self, file_path, filename):
        self.__cluster.load(file_path)

        self.__script_tree.itemSelectionChanged.disconnect()
        self.__script_tree.clear()
        self.__script_tree.itemSelectionChanged.connect(lambda: self.__show_details(self.__script_tree.currentItem()))

        self.__tree_root = self.add_script_root()
        self.__script_tree.expandItem(self.__tree_root)

        self.__editor_tabs.hide()

        for key, value in self.__cluster.get_phm_scripts().items():
            if key[:1] != "__" and key[-2:] != "__":
                self.add_script_child(self.__tree_root, value.get_title())

    def __create_new_script(self, item, col):
        try:
            new_script = self.__cluster.add_script("[\n    {\n        \"\": \"\"\n    }\n]", item.text(col), "Default")
        except Exception as err:
            settings.__LOG__.logError("EDIT_WIDG_ERR:" + str(err))
            return

        if self.__editor_tabs.isHidden():
            self.__editor_tabs.show()

        index = self.__editor_tabs.add_editor(new_script)
        self.__editor_tabs.widget(index).set_tree_item(item)

    def add_new_script(self):
        item = self.add_script_child(self.__tree_root, "")

        self.__script_tree.setCurrentItem(item)
        self.__script_tree.editItem(item)

    def load_script(self):
        file_name, file_path = load_script()
        try:
            new_script = self.__cluster.add_script(text_style.read_text(file_path), file_name, "Dwayne W")
        except Exception as err:
            settings.__LOG__.logError("EDIT_WIDG_ERR: " + str(err))
            return

        item = self.add_script_child(self.__tree_root, file_name)

        if self.__editor_tabs.isHidden():
            self.__editor_tabs.show()

        index = self.__editor_tabs.add_editor(new_script)
        self.__editor_tabs.widget(index).set_tree_item(item)

        return new_script, item

    def __init_script_tree(self):
        self.__tree_root = None

        self.__script_tree = PhtmTreeWidget()
        self.__script_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__script_tree.setColumnCount(1)
        self.__script_tree.setContentsMargins(0, 50, 0, 0)
        self.__script_tree.setHeaderHidden(True)

        self.__script_tree.itemDelegate().closeEditor.connect(self.__editor_closed)

        self.__script_tree_details_box = PhtmPlainTextEdit()
        self.__script_tree_details_box.setReadOnly(True)
        self.__script_tree_details_box.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        self.__script_tree_layout = QVBoxLayout()
        self.__script_tree_layout.addWidget(self.__script_tree)
        self.__script_tree_layout.addWidget(self.__script_tree_details_box)

        self.__script_tree_widget = QWidget()
        self.__script_tree_widget.setLayout(self.__script_tree_layout)
        self.__script_tree_layout.setContentsMargins(0, 26, 0, 0)

        self.__script_tree.itemDoubleClicked.connect(self.__open_script)
        self.__script_tree.itemSelectionChanged.connect(lambda: self.__show_details(self.__script_tree.currentItem()))

        self.__tree_root = self.add_script_root()
        self.__script_tree.setCurrentItem(self.__tree_root)

        self.__script_tree.setHeaderLabels(["Script Cluster"])
        self.__script_tree.expandItem(self.__tree_root)

        self.__script_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__script_tree.customContextMenuRequested.connect(self.on_treeWidget_customContextMenuRequested)

        self.__splitter.addWidget(self.__script_tree_widget)

    def __editor_closed(self, editor, hint):
        item = self.__script_tree.currentItem()
        if editor.text() and not editor.text().isspace():
            if not self.name_temp:
                self.__create_new_script(item, 0)
                return

            if item == self.__tree_root:
                self.__cluster.get_phm().set_name(editor.text())
                self.name_temp = None
                # self.parent.updateWindowTitle(editor.text())
                return

            if not item.text(0):
                item.setText(0, self.name_temp)
            
            print(item.text(0))
            self.__cluster.get_phm_scripts()[item.text(0)] = self.__cluster.get_phm_scripts()[self.name_temp]
            self.__cluster.get_phm_scripts()[item.text(0)].set_title(item.text(0))
            del self.__cluster.get_phm_scripts()[self.name_temp]

            i = self.__editor_tabs.tab_by_text(self.name_temp)
            if i != -1:
                self.__editor_tabs.setTabText(i, item.text(0))

        elif self.name_temp:
            item.setText(0, self.name_temp)
        else:
            self.__tree_root.removeChild(item)

        self.name_temp = None

    def __show_details(self, item):
        if not item or not item.text(0):
            return

        if item != self.__tree_root:
            txt = item.text(0)
            if item.text(0)[0:2] == "* ":
                txt = item.text(0)[2:]
    
            curr_scirpt = self.__cluster.get_phm_scripts()[txt]

            details = "Title: " + curr_scirpt.get_title()
            details += "\nDate Created: " +  str(curr_scirpt.get_date_time_created())
            details += "\nDate Modified: " + str(curr_scirpt.get_date_time_modified())
            details += "\nCreated By: " + curr_scirpt.get_creator()
            details += "\nLast Modified By: " + curr_scirpt.get_modified_by()

        else:
            details = "Title: " + item.text(0)
            details += "\nFile Path: " + self.__cluster.get_file_path()

        self.__script_tree_details_box.setPlainText(details)

    def delete_script(self, index):
        item = self.__tree_root.child(index)
        self.__editor_tabs.close_tab(self.__editor_tabs.tab_by_text(item.text(0)))
        del self.__cluster.get_phm_scripts()[item.text(0)]
        self.__tree_root.removeChild(item)

    def rename_script(self, index):
        item = self.__tree_root.child(index)
        self.__script_tree.editItem(item)
        self.name_temp = item.text(0)

    def on_treeWidget_customContextMenuRequested(self, pos):
        item = self.__script_tree.itemAt(pos)
        self.__script_tree.itemClicked.emit(item, 0)
        if item:
            menu = QMenu(self)
            if self.__script_tree.indexOfTopLevelItem(item) == -1:

                index = item.parent().indexOfChild(item)
                renameAction = QAction("Rename", self)
                renameAction.triggered.connect(lambda x: self.rename_script(index))

                deleteAction = QAction("Delete", self)
                deleteAction.triggered.connect(lambda x: self.delete_script(index))

                menu.addAction(renameAction)
                menu.addAction(deleteAction)

                menu.addSeparator()

                openAction = QAction("Open", self)
                openAction.triggered.connect(lambda x: self.__open_script(self.__script_tree.selectedItems()[0]))

                openTabAction = QAction("Open In New Tab", self)
                openTabAction.triggered.connect(lambda x: self.__open_script_in_tab(self.__script_tree.selectedItems()[0]))

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
                newAction.triggered.connect(lambda x: self.rename_script_root())
                menu.addAction(newAction)

                newAction = QAction("New Script", self)
                newAction.triggered.connect(lambda x: self.add_new_script())
                menu.addAction(newAction)

                menu.addSeparator()

                runAllAction = QAction("Run All", self)
                runAllAction.triggered.connect(lambda: self.parent.r_ctrl.run(1))
                menu.addAction(runAllAction)

            menu.popup(self.__script_tree.viewport().mapToGlobal(pos))

    def rename_script_root(self, name=None):
        if not name:
            self.name_temp = self.__tree_root.text(0)
            self.__script_tree.editItem(self.__tree_root)
        self.__tree_root.setText(0, name)

    def add_script_root(self):
        tree_item = QTreeWidgetItem(self.__script_tree)
        tree_item.setText(0, self.__cluster.get_phm().get_name())
        tree_item.setFlags(tree_item.flags() | Qt.ItemIsEditable)
        tree_item.setIcon(0, QIcon(settings.__ICONS__.white_dot))
        return tree_item

    def add_script_child(self, root, name):
        tree_item = QTreeWidgetItem(root)
        tree_item.setText(0, name)
        tree_item.setFlags(tree_item.flags() | Qt.ItemIsEditable)
        root.addChild(tree_item)
        return tree_item

    def get_script_tree(self):
        return self.__script_tree

    def get_editor_tabs(self):
        return self.__editor_tabs

    def get_cluster(self):
        return self.__cluster

    def save_phm(self, file_path):
        self.parent.statusBar().showMessage("Saving PHM ...")
        for i in range(self.__editor_tabs.count()):
            self.__editor_tabs.save_editor(i)

        self.__cluster.save(file_path)

        filename_w_ext = os.path.basename(file_path)
        filename = os.path.splitext(filename_w_ext)[0]

        if self.__tree_root.text(0) == "New Cluster":
            self.rename_script_root(filename)
            self.parent.updateWindowTitle(filename)
