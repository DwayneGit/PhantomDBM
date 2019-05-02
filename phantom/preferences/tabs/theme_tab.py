from os import listdir
from os.path import isfile, join

import json
from phantom.application_settings import settings

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 

class theme_tab(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.mw=mw
        mypath = "phantom/application_settings/themes/"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        
        self.selected_theme = None

        for f in onlyfiles:
            try:
                self.layout().addWidget(self.create_theme_obj(mypath+f))
            except Exception as err:
                continue
                # print(f + " not a theme.\n" + str(err))
        # self.layout().addWidget(self.create_theme_obj())
        # print(onlyfiles)

    def create_theme_obj(self, fp=None):
        scheme = json.load(open(fp))["color_scheme"]
        
        block = QWidget()
        block.setLayout(QHBoxLayout())
        block.layout().setContentsMargins(0, 0, 0, 0)

        # scheme = {"blue":Qt.blue, "red":Qt.red, "green":Qt.green, "black":Qt.black}

        for key in scheme:
            b = QWidget()
            b.setObjectName("scheme")
            b.setFocusPolicy(Qt.ClickFocus)

            p = QPalette()
            p.setColor(QPalette.Background, QColor(scheme[key]))
            b.setAutoFillBackground(True)
            b.setPalette(p)
            block.layout().addWidget(b)

            b.mousePressEvent = (lambda e: self.load_theme(fp))

        return block

    def load_theme(self, file):
        self.selected_theme = file
