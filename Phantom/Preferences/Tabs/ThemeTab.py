from os import listdir
from os.path import isfile, join

import json

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsWidget, QGraphicsLinearLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

from Phantom.ApplicationSettings import Settings

class ThemeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        mypath = "Phantom/ApplicationSettings/Themes/"

        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        self.selectedTheme = None

        for f in onlyfiles:
            try:
                if f[-4:] == "json":
                    self.layout().addWidget(_ThemeBlock(mypath+f, self))
            except Exception as err:
                Settings.__LOG__.logError(f + " not a theme.\n" + str(err))

class _ThemeBlock(QGraphicsView):
    def __init__(self, fp, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.__theme = json.load(open(fp))

        scene = QGraphicsScene()

        self.setScene(scene)
        self.setStyleSheet("background: transparent")

        self.scale(1, 3)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        block = QGraphicsWidget()
        block.setLayout(QGraphicsLinearLayout())
        block.layout().setContentsMargins(0, 0, 0, 0)
        block.layout().setSpacing(0)
        
        block.setObjectName("scheme")
        block.setFocusPolicy(Qt.ClickFocus)
        block.mousePressEvent = (lambda e: self.loadTheme(fp))

        for key in self.__theme["color_scheme"]:
            b = QGraphicsWidget()
            b.setAutoFillBackground(True)

            p = QPalette()
            p.setColor(QPalette.Background, QColor(self.__theme["color_scheme"][key]))

            b.setPalette(p)

            block.layout().addItem(b)

        # name = QGraphicsTextItem()
        # name.setDefaultTextColor(QColor(self.__theme["color_scheme"]["text"]))
        # name.setPos(150, 15)
        # name.setPlainText(self.__theme["name"])

        scene.addItem(block)
        # scene.addItem(name)

    def loadTheme(self, file):
        self.parent.selectedTheme = file
