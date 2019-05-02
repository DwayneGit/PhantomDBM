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
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setStretch(0, 0)

        self.mw=mw
        mypath = "phantom/application_settings/themes/"

        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        
        self.selected_theme = None

        for f in onlyfiles:
            try:
                self.layout().addWidget(self.create_theme_obj(mypath+f))
            except Exception as err:
                # continue
                print(f + " not a theme.\n" + str(err))
        # self.layout().addWidget(self.create_theme_obj())
        # print(onlyfiles)

    def create_theme_obj(self, fp=None):
        theme = json.load(open(fp))

        scene = QGraphicsScene()
        view = QGraphicsView(scene)
        view.setStyleSheet("background: transparent")

        block = QGraphicsWidget()
        block.setLayout(QGraphicsLinearLayout())
        block.layout().setContentsMargins(0, 0, 0, 0)
        block.layout().setSpacing(0)

        # scheme = {"blue":Qt.blue, "red":Qt.red, "green":Qt.green, "black":Qt.black}
        
        for key in theme["color_scheme"]:
            b = QGraphicsWidget()
            b.setObjectName("scheme")
            b.setFocusPolicy(Qt.ClickFocus)
            b.setAutoFillBackground(True)

            p = QPalette()
            p.setColor(QPalette.Background, QColor(theme["color_scheme"][key]))

            b.setPalette(p)
            b.mousePressEvent = (lambda e: self.load_theme(fp))

            block.layout().addItem(b)

        name = QGraphicsTextItem()
        name.setDefaultTextColor(QColor(theme["color_scheme"]["text"]))
        name.setPos(150,15)
        name.setPlainText(theme["name"])

        scene.addItem(block)
        scene.addItem(name)

        return view

    def load_theme(self, file):
        self.selected_theme = file
