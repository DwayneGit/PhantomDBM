import os
import json
import re

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication

from phantom.logging_stuff import PhtmLogger

from .phtm_icons import PhtmIcons
from .themes.template import styleSheetTemplate as sst

def init(app, settingsFile):

    global __LOG__, __ICONS__, __THEME__
    global __STYLESHEET__, __APPLICATION_SETTINGS__, styleSignal
    global __DATABASE__

    __LOG__ = PhtmLogger()
    __ICONS__ = PhtmIcons()
    __APPLICATION_SETTINGS__ = _Settings(settingsFile)
    __STYLESHEET__, __THEME__ = build_theme(__APPLICATION_SETTINGS__.getSettings()["theme"])
    __DATABASE__ = None

    styleSignal = _StyleChanged(app)

    try:
        userPaths = os.environ['PYTHONPATH'].split(os.pathsep)
    except KeyError as err:
        __LOG__.logError(str(err))
        userPaths = []

    __LOG__.logDebug(userPaths)

class _Settings():
    def __init__(self, settingsFile):
        self.settingsFile = settingsFile
        if not os.path.exists(self.settingsFile):
            self.__setDefaultSettings()
            
        self.settingsJson = json.load(open(self.settingsFile))

    def getSettings(self):
        return self.settingsJson

    def updateSettings(self):
        with open(self.settingsFile, 'w+') as sttngs:
            json.dump(self.settingsJson,
                      sttngs,
                      indent=4,
                      separators=(',', ': '))

    def __setDefaultSettings(self):
        sttngs = {
            'theme':"phantom/application_settings/themes/1_dark.json", 
            "recent_files":[]
        }
        json.dump(sttngs, open(self.settingsFile, 'w+'), indent=4, separators=(',', ': '))

def build_theme(fp):
    styleSheet = ""

    try:
        theme = json.load(open(fp))
    except FileNotFoundError as err:
        __LOG__.logError(str(err))
        __ICONS__.setIconSet("std_black")
        return "", {"file":"", "color_scheme": ""}

    theme["file"] = fp

    __ICONS__.setIconSet(theme["icon_set"])

    p = re.compile('@\w+')

    for line in sst.STYLESHEETTEMPLATE.splitlines():
        if p.search(line):
            if p.search(line).group() == "@close_icon":
                styleSheet += line.replace("@close_icon", __ICONS__.getCloseTab())
            else:
                key = p.search(line).group()
                styleSheet += line.replace(key, theme["color_scheme"][key[1:]])
        else:
            styleSheet += line

    return styleSheet, theme

class _StyleChanged(QObject):
    styleChanged = pyqtSignal(str)
    iconSignal = pyqtSignal()
    def __init__(self, app):
        super().__init__()
        self.connectSignal(app)

    def connectSignal(self, app):
        self.styleChanged.connect(lambda theme: self.setTheme(app, theme))

    @pyqtSlot(QApplication, str)
    def setTheme(self, app, theme):
        global __STYLESHEET__, __THEME__ 
        __STYLESHEET__, __THEME__ = build_theme(theme)
        app.setStyleSheet(__STYLESHEET__)
        self.iconSignal.emit()
