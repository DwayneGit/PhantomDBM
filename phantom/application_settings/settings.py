import os

from .phtm_icons import PhtmIcons
from phantom.logging_stuff import PhtmLogger

def init():
    global __LOG__, __ICONS__, __THEME__
    __LOG__ = PhtmLogger()
    __ICONS__ = PhtmIcons()

    style_sheet = "phantom/application_settings/themes/dark_theme.qss"
    with open(style_sheet, "r") as style_fp:
        __THEME__ = style_fp.read()

    try:
        user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    except KeyError as err:
        __LOG__.logError(str(err))
        user_paths = []

    __LOG__.logDebug(user_paths)
