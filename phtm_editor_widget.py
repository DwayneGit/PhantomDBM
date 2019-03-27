from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from datetime import datetime

from phtm_editor import phtm_editor
from style.phtm_tab_widget import phtm_tab_widget

class phtm_editor_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(0,0,0,0)

        self.__init_script_tree()

        self.__splitter = QSplitter()

        self.__editor_tabs = phtm_tab_widget(self)
        self.__editor_tabs.add_editor()

        self.__editor_tabs.setMovable(True)
        self.__editor_tabs.setTabsClosable(True)

        # self.__layout.addWidget(self.__script_tree_widget)

        self.__splitter.addWidget(self.__editor_tabs)
        self.__splitter.addWidget( self.__script_tree_widget)
        self.__layout.addWidget(self.__splitter)

        self.setLayout(self.__layout)

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

        self.__script_tree.setHeaderLabels(["Title", "Date Created"])
        self.__script_tree.expandItem(self.__tree_root)

        self.add_script_child(self.__tree_root, "Hello", "world")

    def __open_script(self, tree_item):
        print("Opening Json Script...")

    def add_script_root(self, name="New Cluster", description=str(datetime.now())):
        tree_item = QTreeWidgetItem(self.__script_tree)
        tree_item.setText(0, name)
        tree_item.setText(1, description)
        return tree_item

    def add_script_child(self, root, name, description):
        tree_item = QTreeWidgetItem()
        tree_item.setText(0, name)
        tree_item.setText(1, description)

        root.addChild(tree_item)

    def get_script_tree(self):
        return self.__script_tree

    def get_editor_tabs(self):
        return self.__editor_tabs

    def getPermanentTitle(self):
        return self.parent.parent.getPermanentTitle()
