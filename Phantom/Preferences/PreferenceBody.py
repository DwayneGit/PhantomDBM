import json
from copy import deepcopy

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from Phantom.PhtmWidgets import PhtmPushButton, PhtmTabWidget, PhtmTitleBar

from Phantom.ApplicationSettings import Settings

from Phantom.Utility import centerWindow

from .Tabs.DatabaseTab import DatabaseTab
from .Tabs.DmiTab import DmiTab
from .Tabs.SchemaTab import SchemaTab
from .Tabs.ThemeTab import ThemeTab

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

        self.__titleBar = PhtmTitleBar(self)
        self.__titleBar.generateTitleBar()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)

        self.__layout.addWidget(self.__titleBar)

        self.initPreferenceBody()
        self.__layout.addWidget(self.prefBody)

        self.setLayout(self.__layout)

        self.setGeometry(QRect(10, 10, 450, 500),)
        self.move(centerWindow(self))

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(30, 30, 30))
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3)
        self.setGraphicsEffect(self.shadow)

        self.setDialogWindowTitle(self.windowTitle)

    def setDialogWindowTitle(self, text):
        self.__titleBar.setWindowTitle(text)
        self.setWindowTitle(text)
    
    def getWindowTitle(self):
        return self.__titleBar.windowTitle

    def getLayout(self):
        return self.__layout

    def initPreferenceBody(self):
        self.prefBody = QDialog()
        vBox = QVBoxLayout()

        self.svd = False
 
        self.instancesPrefDict = deepcopy(Settings.__DATABASE__)

        self.dmiTab = DmiTab(self.__cluster)
        self.schemaTab = SchemaTab(self.__cluster.getPhmScripts()["__schema__"])
        self.databaseTab = DatabaseTab(self.instancesPrefDict)
        self.themeTab = ThemeTab()

        self.tabW = PhtmTabWidget(self)
        self.tabW.setTabPosition(QTabWidget.North)

        self.tabW.addTab(self.databaseTab, "Database")
        self.tabW.addTab(self.dmiTab, "DMI")
        self.tabW.addTab(self.schemaTab, "Schema")
        # self.tabW.addTab(userTab(), "User")
        self.tabW.addTab(self.themeTab, "Theme")

        vBox.addWidget(self.tabW)
        vBox.addWidget(self.buttons())

        self.prefBody.setLayout(vBox)

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

        self.dmiTab.saveDmi()
        
        if not self.schemaTab.saveSchemas():
            return False
        self.__cluster.setChildren(self.schemaTab.children)

        self.svd = True

        if self.themeTab.selectedTheme and Settings.__THEME__["file"] != self.themeTab.selectedTheme:
            Settings.styleSignal.styleChanged.emit(self.themeTab.selectedTheme)
            Settings.__APPLICATION_SETTINGS__.getSettings()["theme"] = self.themeTab.selectedTheme
            Settings.__APPLICATION_SETTINGS__.updateSettings()

        return True

    def submitPreferences(self):
        if self.savePreferences():
            self.accept()

    def cancelPreferences(self):
        if not self.svd:
            self.reject() #if canceled with out previously being saved
        else:
            self.accept()
