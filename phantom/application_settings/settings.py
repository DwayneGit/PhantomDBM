import os
import json
import fileinput
import re

from .phtm_icons import PhtmIcons
from phantom.logging_stuff import PhtmLogger

def init(stngs_file=None):
    stngs_json = json.load(open(stngs_file))
    
    global __LOG__, __ICONS__, __THEME__, __STYLESHEET__
    
    __LOG__ = PhtmLogger()
    __ICONS__, __STYLESHEET__, __THEME__ = build_theme(stngs_json["theme"])
    
    try:
        user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    except KeyError as err:
        __LOG__.logError(str(err))
        user_paths = []

    __LOG__.logDebug(user_paths)

def build_theme(fp):
    style_sheet = ""

    theme = json.load(open(fp))
    icon_set = PhtmIcons(theme["icon_set"])
    
    with fileinput.input(files=("phantom/application_settings/themes/theme_template.qss")) as f:
        p = re.compile('@\w+')
        for line in f:
            if p.search(line):
                key = p.search(line).group()
                style_sheet += line.replace(key, theme["color_scheme"][key[1:]] )
                # print(theme["color_scheme"][key[1:]])
            else:
                style_sheet += line
    
    return icon_set, style_sheet, theme