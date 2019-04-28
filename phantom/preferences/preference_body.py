from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QTabWidget, QWidget, QHBoxLayout

import json

from phantom.phtm_widgets import PhtmPushButton
from phantom.phtm_widgets import PhtmTabWidget

from .tabs.database_tab import database_tab
from .tabs.dmi_tab import dmi_tab
from .tabs.schema_tab import schema_tab
from .tabs.theme_tab import theme_tab

class preference_body(QDialog):
    def __init__(self, user, log, parent):
        super(preference_body, self).__init__()

        self.user = user
        self.svd = False
        self.log = log
        self.parent = parent

        self.prefs = self.parent.parent.get_editor_widget().get_cluster().get_settings()
        self.instancesPrefDict = self.prefs

        self.dmiTab = dmi_tab(self.parent.parent)
        self.schemaTab = schema_tab(self.parent.parent.get_editor_widget().get_cluster().get_phm_scripts()["__schema__"],
                                        self.parent.parent.get_editor_widget().get_cluster().get_phm_scripts()["__reference_schemas__"])
        self.databaseTab = database_tab(self.prefs, self.instancesPrefDict, self.parent.parent.log)
        self.themeTab = theme_tab()

        self.initUI()

    def initUI(self):
        vBox = QVBoxLayout()

        self.tabW = PhtmTabWidget(self)
        self.tabW.setTabPosition(QTabWidget.North)

        self.tabW.addTab(self.databaseTab, "Database")
        self.tabW.addTab(self.dmiTab, "DMI")
        self.tabW.addTab(self.schemaTab, "Schema")
        # self.tabW.addTab(userTab(), "User")
        self.tabW.addTab(self.themeTab, "Theme")

        vBox.addWidget(self.tabW)
        vBox.addWidget(self.buttons())

        self.setLayout(vBox)

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
        self.parent.prefs = self.databaseTab.save(self.prefs)
        self.parent.parent.get_editor_widget().get_cluster().save_settings(self.parent.prefs)

        self.dmiTab.save_dmi()
        if not self.schemaTab.save_schemas():
            return False
        self.svd = True
        return True

    def submitPreferences(self):
        if self.savePreferences():
            self.parent.accept()

    def cancelPreferences(self):
        if not self.svd:
            self.parent.reject() #if canceled with out previously being saved
        else:
            self.parent.accept()

    def getWindowTitle(self):
        return self.parent.getWindowTitle()

    def set_window_title(self, text):
        self.parent.set_window_title(text)