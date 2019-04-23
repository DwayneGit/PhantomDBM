import re

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from phtm_editor import phtm_editor
from phtm_widgets.phtm_main_window import phtm_main_window
from phtm_widgets.phtm_tab_widget import phtm_tab_widget
from file.json_script import json_script

class tab_widget(phtm_tab_widget):
    def __init__(self, parent=None):
        super().__init__()

        self.default_tab_count = 1
        self.parent = parent
        self.tab_data = {}