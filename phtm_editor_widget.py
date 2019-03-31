import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from datetime import datetime
from file.phm_file_handler import phm_file_handler
from file.json_script import json_script

from phtm_widgets.phtm_tree_widget import phtm_tree_widget
from phtm_widgets.phtm_plain_text_edit import phtm_plain_text_edit

from phtm_editor import phtm_editor
from tab_widget import tab_widget

import run_ctrl as r_ctrl

class phtm_editor_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent
        self.cluster = phm_file_handler()

        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)

        self.__splitter = QSplitter()

        self.__init_editor()
        self.__init_script_tree()
        
        self.__default_count = 0
        self.add_defualt_script()

        self.file_path = ""

        self.name_temp = None

        # self.__layout.addWidget(self.__script_tree_widget)
        self.__splitter.setSizes([200, 150])
        self.__layout.addWidget(self.__splitter)

        self.setLayout(self.__layout)

    def __init_editor(self):

        self.__editor_tabs = tab_widget(self)

        self.__editor_tabs.setMovable(True)
        self.__editor_tabs.setTabsClosable(True)

        self.__editor_tabs.tabCloseRequested.connect(self.__tabs_closed)

        self.__splitter.addWidget(self.__editor_tabs)

    def __tabs_closed(self):
        # print("tab being closed..")
        if self.__editor_tabs.count() < 1:
            self.__editor_tabs.hide()

    def clear_tabs(self):
        self.__editor_tabs.clear()

    def __open_script(self, item):
        #self.cluster.get_phm_scripts()[hash(tree_item.text(0))] # load double clicked script int self.__editor_tabs
        # print(self.cluster.get_phm_scripts().keys())
        # print(hash(tree_item.text(0)))
        if item == self.__tree_root or (self.__editor_tabs.tab_by_text(item.text(0)) != -1):
            return

        if self.__editor_tabs.isHidden():
            self.__editor_tabs.show()
            self.__editor_tabs.add_editor()

        self.__editor_tabs.currentWidget().set_curr_script(self.cluster.get_phm_scripts()[hash(item.text(0))])
        self.__editor_tabs.setTabText(self.__editor_tabs.currentIndex(), item.text(0))
        # print("Opening Json Script...")

    def __open_script_in_tab(self, tree_item):
        #self.cluster.get_phm_scripts()[hash(tree_item.text(0))] # load double clicked script int self.__editor_tabs
        # print(self.cluster.get_phm_scripts().keys())
        # print(hash(tree_item.text(0)))
        self.__editor_tabs.add_editor(self.cluster.get_phm_scripts()[hash(tree_item.text(0))])
        # print("Opening Json Script...")

    def load_cluster(self, file_path):
        self.__script_tree.itemChanged.disconnect()
        self.cluster.load(file_path)
        self.__script_tree.clear()

        self.file_path = file_path

        filename_w_ext = os.path.basename(file_path)
        filename, file_extension = os.path.splitext(filename_w_ext)
        #filename = foobar
        #file_extension = .txt

        self.__tree_root = self.add_script_root(filename)
        self.__script_tree.expandItem(self.__tree_root)
        
        # print(self.cluster.get_phm_scripts())

        for key, value in self.cluster.get_phm_scripts().items():
            # print(value.get_title())
            self.add_script_child(self.__tree_root, value.get_title())

        self.__script_tree.itemChanged.connect(self.item_changed)

    def add_defualt_script(self):
        title = "JSON Template"
        if self.__default_count >= 1:
            title += " " + str(self.__default_count)

        default = self.add_script("[\n    {\n        \"\": \"\"\n    }\n]", title, "Default")
    
        if self.__editor_tabs.isHidden():
            self.__editor_tabs.show()

        self.__editor_tabs.add_editor(self.cluster.get_phm_scripts()[hash(title)])
        self.__default_count += 1

    def add_script(self, script, title, creator):
        new_script = self.cluster.add_script(script, title, creator)
        self.__script_tree.itemChanged.disconnect()
        self.add_script_child(self.__tree_root, title)
        self.__script_tree.itemChanged.connect(self.item_changed)

        return new_script

    def __init_script_tree(self):

        self.__tree_root = None

        self.__script_tree = phtm_tree_widget()
        self.__script_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__script_tree.setColumnCount(1)
        # self.__script_tree.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # self.__script_tree.setFixedWidth(200)
        self.__script_tree.setContentsMargins(0,50,0,0)
        # self.__script_tree.setHeaderHidden(True)

        self.__script_tree_details_box = phtm_plain_text_edit()
        self.__script_tree_details_box.setReadOnly(True)

        self.__script_tree_layout = QVBoxLayout()
        self.__script_tree_layout.addWidget(self.__script_tree)
        self.__script_tree_layout.addWidget(self.__script_tree_details_box)

        self.__script_tree_widget = QWidget()
        self.__script_tree_widget.setLayout(self.__script_tree_layout)
        self.__script_tree_layout.setContentsMargins(0,26,0,0)

        self.__script_tree.itemDoubleClicked.connect(self.__open_script)
        self.__script_tree.itemClicked.connect(self.__show_details)

        self.__tree_root = self.add_script_root()

        self.__script_tree.setHeaderLabels(["Script Cluster"])
        self.__script_tree.expandItem(self.__tree_root)

        self.__script_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__script_tree.customContextMenuRequested.connect(self.on_treeWidget_customContextMenuRequested)

        self.__script_tree.itemChanged.connect(self.item_changed)
        # self.add_script_child(self.__tree_root, "Hello", "cruel", "world")

        self.__splitter.addWidget( self.__script_tree_widget)

    def __show_details(self, item):
        if not item:
            return
            
        if item != self.__tree_root:
            curr_scirpt = self.cluster.get_phm_scripts()[hash(item.text(0))]

            details = "Title: " + curr_scirpt.get_title()
            details += "\nDate Created: " +  str(curr_scirpt.get_date_time_created())
            details += "\nDate Modified: " + str(curr_scirpt.get_date_time_modified())
            details += "\nCreated By: " + curr_scirpt.get_creator()
            details += "\nLast Modified By: " + curr_scirpt.get_modified_by()

        else:

            details = "Title: " + item.text(0)
            details += "\nFile Path: " + self.file_path

        self.__script_tree_details_box.setPlainText(details)
            # details += "\nDate Created: " + curr_scirpt.

    def delete_script(self, index):
        item = self.__tree_root.child(index)
        del self.cluster.get_phm_scripts()[hash(item.text(0))]
        self.__tree_root.removeChild(item)

    def rename_script(self, index):
        item = self.__tree_root.child(index)
        self.__script_tree.editItem(item)
        self.name_temp = item.text(0)
    
    def item_changed(self, item, col):
        # print(item.text(0))
        # print(col)
        if col != 0:
            return

        self.cluster.get_phm_scripts()[hash(item.text(0))] = self.cluster.get_phm_scripts()[hash(self.name_temp)]
        self.cluster.get_phm_scripts()[hash(item.text(0))].set_title(item.text(0))
        del self.cluster.get_phm_scripts()[hash(self.name_temp)]
        self.name_temp = None

    def on_treeWidget_customContextMenuRequested(self, pos):
        item = self.__script_tree.itemAt(pos)
        self.__script_tree.itemClicked.emit(item, 0)
        # print(str(self.__script_tree.indexOfTopLevelItem(item)))
        if item:
            menu=QMenu(self)
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
                runAction.triggered.connect(lambda x: r_ctrl.run_script(self.parent))

                runBelow = QAction("Run + Scripts Below", self)
                runBelow.triggered.connect(lambda x: r_ctrl.run_plus_below(self.parent, index))

                menu.addAction(runAction)
                menu.addAction(runBelow)
            
            else:
                # print(index)
                newAction = QAction("New Script", self)
                newAction.triggered.connect(lambda x: self.add_defualt_script())
                menu.addAction(newAction)

                menu.addSeparator()

                runAllAction = QAction("Run All", self)
                runAllAction.triggered.connect(lambda x: r_ctrl.run_all_scripts(self.parent))
                menu.addAction(runAllAction)

            menu.popup(self.__script_tree.viewport().mapToGlobal(pos))

    def rename_script_root(self, name):
        self.__tree_root.setText(0, name)

    def add_script_root(self, name="New Cluster"):
        tree_item = QTreeWidgetItem(self.__script_tree)
        tree_item.setText(0, name)
        return tree_item

    def add_script_child(self, root, name):
        tree_item = QTreeWidgetItem(root)
        tree_item.setText(0, name)
        tree_item.setFlags(tree_item.flags() | Qt.ItemIsEditable)

        root.addChild(tree_item)

    def get_script_tree(self):
        return self.__script_tree

    def get_editor_tabs(self):
        return self.__editor_tabs

    def get_cluster(self):
        return self.cluster

    def getPermanentTitle(self):
        return self.parent.parent.getPermanentTitle()
