import os

from .phtm_icons import PhtmIcons
from .logging_stuff import PhtmLogger

def init():

    global __LOG__, __ICONS__
    __LOG__ = PhtmLogger()
    __ICONS__ = PhtmIcons()

    try:
        user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    except KeyError as err:
        __LOG__.logError(str(err))
        user_paths = []

    __LOG__.logDebug(user_paths)
