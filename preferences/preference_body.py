from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 

from utility.center import center_window
from database.DBConnection import *

import file_ctrl as f_ctrl

from phtm_widgets.phtm_push_button import phtm_push_button
from phtm_widgets.phtm_combo_box import phtm_combo_box
from phtm_widgets.phtm_tab_widget import phtm_tab_widget
from phtm_widgets.phtm_plain_text_edit import phtm_plain_text_edit

from preferences.tabs.database_tab import database_tab
from preferences.tabs.dmi_tab import dmi_tab
from preferences.tabs.schema_tab import schema_tab
from preferences.tabs.theme_tab import theme_tab

class preference_body(QDialog):
    def __init__(self, user, log, parent):
        super(preference_body, self).__init__()
        '''
        Initialize the window
        '''
        
        self.user = user
        self.svd = False
        self.log = log
        self.parent = parent
        
        self.prefs = self.parent.parent.get_editor_widget().get_cluster().get_settings()
        self.instancesPrefDict = self.prefs

        self.dmiTab = dmi_tab(self.parent.parent)
        self.schemaTab = schema_tab(self.parent.parent)
        self.databaseTab = database_tab(self.prefs, self.instancesPrefDict, self.parent.parent.log)
        self.themeTab = theme_tab()

        self.initUI()

    def initUI(self):
        vBox = QVBoxLayout()

        self.tabW = phtm_tab_widget(self)
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

        saveButton = phtm_push_button("Save")
        saveButton.clicked.connect(self.savePreferences)
        
        submitButton = phtm_push_button("Submit")
        submitButton.clicked.connect(self.submitPreferences)
        
        cancelButton = phtm_push_button("Cancel")
        cancelButton.clicked.connect(self.cancelPreferences)

        btnLayout.addWidget(saveButton)
        btnLayout.addWidget(submitButton)
        btnLayout.addWidget(cancelButton)

        btnWidget.setLayout(btnLayout)
        return btnWidget

    def savePreferences(self):
        self.saveDbTab()
        try:
            self.schemaTab.save_schemas()
        except ValueError as err:
            self.parent.parent.log.logError(err)
            return False
        self.svd = True
        return True

    def saveDbTab(self):
        if self.prefs['db'] == "mongodb":
            self.prefs['mongodb']['dbname'] = self.databaseTab.get_db_form().itemAt(3).widget().currentText()

            self.prefs['mongodb']['collection'] = self.databaseTab.get_db_form().itemAt(11).widget().currentText()

            self.prefs['mongodb']['host'] = self.databaseTab.get_db_form().itemAt(5).widget().text()

            self.prefs['mongodb']['port'] = int(self.databaseTab.get_db_form().itemAt(7).widget().text())

            self.prefs['mongodb']['tableSize'] = int(self.databaseTab.get_db_form().itemAt(9).widget().text())

        elif self.prefs['db'] == "sql":
            pass

        self.parent.parent.get_editor_widget().get_cluster().save_settings(self.prefs)
        self.parent.prefs = self.prefs
        
        self.dmiTab.save_dmi()

    def submitPreferences(self):
        if self.savePreferences():
            self.parent.accept()

    def cancelPreferences(self):
        if self.svd == False:
            self.parent.reject() #if canceled with out previously being saved
        else:
            self.parent.accept()

    def getWindowTitle(self):
        return self.parent.getWindowTitle()

    def set_window_title(self, text):
        self.parent.set_window_title(text)

class api_tab(QWidget):
    def __init__(self):
        pass