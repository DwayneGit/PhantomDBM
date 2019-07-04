import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from phantom.phtm_widgets import PhtmPushButton, PhtmTabWidget, PhtmTitleBar

from phantom.application_settings import settings

from phantom.utility import center_window

from .tabs.database_tab import database_tab
from .tabs.dmi_tab import dmi_tab
from .tabs.schema_tab import schema_tab
from .tabs.theme_tab import theme_tab

class preference_body(QDialog):
    def __init__(self, title, geometry, parent, user=None):
        super().__init__() # set screen size (left, top, width, height

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowModality(Qt.ApplicationModal)

        self.window_title = title

        self.parent = parent
        self.user = user

        self.oldPos = self.pos()

        self.title_bar = PhtmTitleBar(self)
        self.title_bar.generate_title_bar()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)

        self.__layout.addWidget(self.title_bar)

        self.pref_body = QDialog()
        self.init_preference_body()
        self.__layout.addWidget(self.pref_body)

        self.setLayout(self.__layout)

        self.setGeometry(geometry)
        self.move(center_window(self))

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(30, 30, 30))
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3)
        self.setGraphicsEffect(self.shadow)

        self.set_window_title(self.window_title)

    def set_window_title(self, text):
        self.title_bar.set_window_title(text)
        self.setWindowTitle(text)
    
    def getWindowTitle(self):
        return self.title_bar.window_title

    def get_layout(self):
        return self.__layout

    def init_preference_body(self):
        vBox = QVBoxLayout()

        self.svd = False

        self.prefs = self.parent.get_editor_widget().get_cluster().get_settings()
        self.instancesPrefDict = self.prefs

        self.dmiTab = dmi_tab(self.parent)
        self.schemaTab = schema_tab(self.parent.get_editor_widget().get_cluster().get_phm_scripts()["__schema__"],
                                    self.prefs['mongodb']['dbname'],
                                    self.prefs['mongodb']['collection'])
        self.databaseTab = database_tab(self.prefs, self.instancesPrefDict)
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
        self.parent.prefs = self.databaseTab.save(self.prefs)
        self.parent.get_editor_widget().get_cluster().save_settings(self.parent.prefs)

        self.dmiTab.save_dmi()
        
        if not self.schemaTab.save_schemas():
            return False
        self.parent.get_editor_widget().get_cluster().set_children(self.schemaTab.children)

        self.svd = True

        if self.themeTab.selected_theme and settings.__THEME__["file"] != self.themeTab.selected_theme:
            settings.style_signal.style_change.emit(self.themeTab.selected_theme)
            settings.__APPLICATION_SETTINGS__.get_settings()["theme"] = self.themeTab.selected_theme
            settings.__APPLICATION_SETTINGS__.update_settings()

        return True

    def submitPreferences(self):
        if self.savePreferences():
            self.accept()

    def cancelPreferences(self):
        if not self.svd:
            self.reject() #if canceled with out previously being saved
        else:
            self.accept()
