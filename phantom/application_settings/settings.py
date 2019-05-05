import os
import json
import fileinput
import re

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication

from phantom.logging_stuff import PhtmLogger
from phantom.database import DatabaseHandler

from .phtm_icons import PhtmIcons
from .themes.template import style_sheet_template as sst

def init( app, stngs_file):
    stngs_json = json.load(open(stngs_file))

    global __LOG__, __ICONS__, __THEME__
    global __STYLESHEET__, __APPLICATION_SETTINGS__, style_signal
    global __DATABASE__

    __LOG__ = PhtmLogger()
    __ICONS__ = PhtmIcons()
    __APPLICATION_SETTINGS__ = stngs_file
    __STYLESHEET__, __THEME__ = build_theme(stngs_json["theme"])
    __DATABASE__ = None

    style_signal = _StyleChanged(app)

    try:
        user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    except KeyError as err:
        __LOG__.logError(str(err))
        user_paths = []

    __LOG__.logDebug(user_paths)

def build_theme(fp):
    style_sheet = ""

    try:
        theme = json.load(open(fp))
    except FileNotFoundError as err:
        __LOG__.logError(str(err))
        __ICONS__.set_icons_set("std_black")
        return "", {"file":"", "color_scheme": ""}

    theme["file"] = fp

    __ICONS__.set_icons_set(theme["icon_set"])

    p = re.compile('@\w+')

    for line in sst.styleSheetTemplate.splitlines():
        if p.search(line):
            if p.search(line).group() == "@close_icon":
                style_sheet += line.replace("@close_icon", __ICONS__.get_close_tab())
            else:
                key = p.search(line).group()
                style_sheet += line.replace(key, theme["color_scheme"][key[1:]])
        else:
            style_sheet += line

    return style_sheet, theme

class _StyleChanged(QObject):
    style_change = pyqtSignal(str)
    icon_signal = pyqtSignal()
    def __init__(self, app):
        super().__init__()
        self.connect_signal(app)

    def connect_signal(self, app):
        self.style_change.connect(lambda theme: self.set_theme(app, theme))

    @pyqtSlot(QApplication, str)
    def set_theme(self, app, theme):
        global __STYLESHEET__, __THEME__ 
        __STYLESHEET__, __THEME__ = build_theme(theme)
        app.setStyleSheet(__STYLESHEET__)
        self.icon_signal.emit()
