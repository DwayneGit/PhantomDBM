import re

from phtm_widgets.phtm_tab_widget import phtm_tab_widget

class tab_widget(phtm_tab_widget):
    def __init__(self, parent=None):
        super().__init__()

        self.default_tab_count = 1
        self.parent = parent
        self.tab_data = {}