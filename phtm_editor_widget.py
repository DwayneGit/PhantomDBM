import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from datetime import datetime
from file.phm_file_handler import phm_file_handler
from file.json_script import json_script

from phtm_editor import phtm_editor
from tab_widget import tab_widget

class phtm_editor_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent
        self.cluster = phm_file_handler()

        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(0,0,0,0)

        self.__splitter = QSplitter()

        self.__init_editor()
        self.__init_script_tree()

        # self.__layout.addWidget(self.__script_tree_widget)
        self.__layout.addWidget(self.__splitter)

        self.setLayout(self.__layout)

    def __init_editor(self):

        self.__editor_tabs = tab_widget(self)
        self.__editor_tabs.add_editor()

        self.__editor_tabs.setMovable(True)
        self.__editor_tabs.setTabsClosable(True)

        self.__splitter.addWidget(self.__editor_tabs)

    def __open_script(self, tree_item):
        #self.cluster.get_phm_scripts()[hash(tree_item.text(0))] # load double clicked script int self.__editor_tabs
        # print(self.cluster.get_phm_scripts().keys())
        # print(hash(tree_item.text(0)))
        self.__editor_tabs.add_editor(self.cluster.get_phm_scripts()[hash(tree_item.text(0))])
        print("Opening Json Script...")

    def load_cluster(self, file_path):
        self.cluster.load(file_path)
        self.__script_tree.clear()

        filename_w_ext = os.path.basename(file_path)
        filename, file_extension = os.path.splitext(filename_w_ext)
        #filename = foobar
        #file_extension = .txt

        self.__tree_root = self.add_script_root(filename, str(self.cluster.get_phm().get_time_modified()), str(self.cluster.get_phm().get_time_created()))
        self.__script_tree.expandItem(self.__tree_root)
        
        # print(self.cluster.get_phm_scripts())

        for key, value in self.cluster.get_phm_scripts().items():
            # print(value.get_title())
            self.add_script_child(self.__tree_root, value.get_title(), str(value.get_date_time_modified()), str(value.get_date_time_created()))

    def add_script(self, script, title, creator):
        new_script = self.cluster.add_script(script,title,creator)
        self.add_script_child(self.__tree_root, title, str(new_script.get_date_time_modified()), str(new_script.get_date_time_created()))
        return new_script

    def __init_script_tree(self):

        self.__tree_root = None

        self.__script_tree = QTreeWidget()
        self.__script_tree.setColumnCount(2)
        # self.__script_tree.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # self.__script_tree.setFixedWidth(200)
        self.__script_tree.setContentsMargins(0,50,0,0)

        self.__script_tree_layout = QVBoxLayout()
        self.__script_tree_layout.addWidget(self.__script_tree)

        self.__script_tree_widget = QWidget()
        self.__script_tree_widget.setLayout(self.__script_tree_layout)
        self.__script_tree_layout.setContentsMargins(0,26,0,0)

        self.__script_tree.itemDoubleClicked.connect(self.__open_script)

        self.__tree_root = self.add_script_root()

        self.__script_tree.setHeaderLabels(["Title", "Date Modified", "Date Created"])
        self.__script_tree.expandItem(self.__tree_root)

        self.add_script_child(self.__tree_root, "Hello", "cruel", "world")

        self.__splitter.addWidget( self.__script_tree_widget)

    def rename_script_root(self, name):
        self.__tree_root.setText(0, name)

    def add_script_root(self, name="New Cluster", date_modified=str(datetime.now()), date_created=str(datetime.now())):
        tree_item = QTreeWidgetItem(self.__script_tree)
        tree_item.setText(0, name)
        tree_item.setText(1, date_modified)
        tree_item.setText(2, date_created)
        return tree_item

    def add_script_child(self, root, name, date_modified, date_created):
        tree_item = QTreeWidgetItem()
        tree_item.setText(0, name)
        tree_item.setText(1, date_modified)
        tree_item.setText(2, date_created)

        root.addChild(tree_item)

    def get_script_tree(self):
        return self.__script_tree

    def get_editor_tabs(self):
        return self.__editor_tabs

    def get_cluster(self):
        return self.cluster

    def getPermanentTitle(self):
        return self.parent.parent.getPermanentTitle()
