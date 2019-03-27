import pickle
import numpy
import json

from datetime import datetime
from collections import OrderedDict

from .json_script import json_script

class phm():

    def __len__(self):
        return len(self.__scripts)

    def __init__(self, scripts=None, creator=None, group=None, access_level=None):
        
        self.__class__ = phm
        self.__class__.__name__ = "phm"

        current_date_time = datetime.now()

        self.__date_time_created = current_date_time
        self.__date_time_modified = current_date_time

        self.__creator = creator
        self.__group = group

        self.__last_modified_by = None
        self.__modify_log = []

        self.__access_level = access_level
        self.__public = True

        if scripts:
            self.__scripts = scripts
        else:
            self.__scripts = OrderedDict()
            
#---------------------------- Access Functions ------------------------------

    def get_scripts(self):
        return self.__scripts

    def modified_by(self, user, script_title=None):
        if script_title:
            self.__scripts[hash(script_title)].set_modified_by()

        self.__last_modified_by = user
        self.__modify_log.append(user)

    def get_last_modified_by(self, script_title=None):
        if script_title:
            return self.__scripts[hash(script_title)]["last_modified_by"][-1]
        return self.__last_modified_by

    def get_access(self, user):
        if user in self.__group or (user.access_level == self.__access_level and self.__access_level):
            return True
        return False

    def get_group(self):
        return self.__group

    def set_group(self, group):
        self.__group = group

    def is_public(self, public):
        self.__public = public
        return self.__public