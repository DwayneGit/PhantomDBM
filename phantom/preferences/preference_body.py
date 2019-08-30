import json
from copy import deepcopy

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from phantom.phtmWidgets import PhtmPushButton, PhtmTabWidget, PhtmTitleBar

from phantom.applicationSettings import settings

from phantom.utility import centerWindow

from .tabs.database_tab import database_tab
from .tabs.dmi_tab import dmi_tab
from .tabs.schema_tab import schema_tab
from .tabs.theme_tab import theme_tab

class PreferenceBody(QDialog):
    def __init__(self, cluster, user=None):
        super().__init__() # set screen size (left, top, width, height

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowModality(Qt.ApplicationModal)

        self.windowTitle = "Preferences"
        
        self.__cluster = cluster
        self.user = user

        self.oldPos = self.pos()

        self.titleBar = PhtmTitleBar(self)
        self.titleBar.generateTitleBar()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)

        self.__layout.addWidget(self.titleBar)

        self.pref_body = QDialog()
        self.init_PreferenceBody()
        self.__layout.addWidget(self.pref_body)

        self.setLayout(self.__layout)

        self.setGeometry(QRect(10, 10, 450, 500),)
        self.move(centerWindow(self))

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(30, 30, 30))
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3)
        self.setGraphicsEffect(self.shadow)

        self.setWindowTitle(self.windowTitle)

    def setWindowTitle(self, text):
        self.titleBar.setWindowTitle(text)
        self.setWindowTitle(text)
    
    def getWindowTitle(self):
        return self.titleBar.windowTitle

    def get_layout(self):
        return self.__layout

    def init_PreferenceBody(self):
        vBox = QVBoxLayout()

        self.svd = False
 
        self.instancesPrefDict = deepcopy(settings.__DATABASE__)

        self.dmiTab = dmi_tab(self.__cluster)
        self.schemaTab = schema_tab(self.__cluster.getPhmScripts()["__schema__"])
        self.databaseTab = database_tab(self.instancesPrefDict)
        self.themeTab = theme_tab()

        self.tabW = PhtmTabWidget(self)
        self.tabW.setTabPosition(QTabWidget.North)

        self.tabW.addTab(self.databaseTab, "Database")
        self.tabW.addTab(self.dmiTab, "DMI")
        self.tabW.addTab(self.schemaTab, "Schema")
        # self.tabW.addTab(userTab(), "User")
        self.tabW.addTab(self.themeTab, "Theme")

        vBox.addWidget(self.tabW)
        vBox.addWidget(self.buttons())

        self.pref_body.setLayout(vBox)

    def buttons(self):
        btnWidget = QWidget()
        btnLayout = QHBoxLayout()

        saveButton = PhtmPushButton("Save")
        saveButton.clicked.connect(self.savePreferences)

        submitButton = PhtmPushButton("Submit")
        submitButton.clicked.connect(self.submitPreferences)

        cancelButton = PhtmPushButton("Cancel")
        cancelButton.clicked.connect(self.cancelPreferences)

        btnLayout.addWidget(saveButton)
        btnLayout.addWidget(submitButton)
        btnLayout.addWidget(cancelButton)

        btnWidget.setLayout(btnLayout)
        return btnWidget

    def savePreferences(self):
        self.databaseTab.save()

        self.dmiTab.save_dmi()
        
        if not self.schemaTab.save_schemas():
            return False
        self.__cluster.set_children(self.schemaTab.children)

        self.svd = True

        if self.themeTab.selected_theme and settings.__THEME__["file"] != self.themeTab.selected_theme:
            settings.styleSignal.styleChanged.emit(self.themeTab.selected_theme)
            settings.__APPLICATION_SETTINGS__.getSettings()["theme"] = self.themeTab.selected_theme
            settings.__APPLICATION_SETTINGS__.updateSettings()

        return True

    def submitPreferences(self):
        if self.savePreferences():
            self.accept()

    def cancelPreferences(self):
        if not self.svd:
            self.reject() #if canceled with out previously being saved
        else:
            self.accept()
