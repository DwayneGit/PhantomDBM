import pickle
import numpy
import json

from datetime import datetime
from collections import OrderedDict

from .json_script import json_script
from .phm import phm as phm_file

class phm_file_handler():

    def __init__(self, phm=None, db_handler=None):
        
        self.__class__ = phm_file_handler
        self.__class__.__name__ = "phm_file_handler"

        # print(type(self))
        self.__file_path = None

        if phm:
            self.__phm = phm
        else:
            self.__phm = phm_file()

        # print(type(self.__phm))

        # current_date_time = datetime.now()

        # self.__date_time_created = current_date_time
        # self.__date_time_modified = current_date_time

        self.__db_handler = db_handler

        # self.__creator = creator
        # self.__group = group

        # self.__last_modified_by = None
        # self.__modify_log = []

        # self.__access_level = access_level
        # self.__public = True

    # self.__scripts = OrderedDict()

    # def __len__(self):
    #     return len(self.__scripts)

    def save(self, file_name=None, user=None):
        self.__phm.modified_by(user)
        pickle.dump(self.__phm, open(file_name + ".phm", "wb"))

    def load(self, file_path):
        self.__file_path = file_path
        self.__phm = pickle.load(open(file_path, "rb" ))

#------------------------- script methods --------------------------
    def add_script(self, script, title=None, creator=None):
        # print(self.get_phm_scripts())
        if hash(title) in self.get_phm_scripts():
            print("Error: script title already exist in this ____(cluster)")
            return False

        new_script = json_script(script, title, creator)

        self.get_phm_scripts()[hash(title)] = new_script

        return new_script

    def get_script(self, title):
        if hash(title) in self.get_phm_scripts():
            return self.get_phm_scripts()[hash(title)]
        return None

    def get_phm(self):
        return self.__phm

    def export_script(self, title, dest, user=None):
        json.dump(self.get_phm_scripts()[hash(title)], dest)

    def get_phm_scripts(self):
        return self.__phm.get_scripts()

    def get_file_path(self):
        return self.__file_path

    def set_file_path(self, file_path):
        self.__file_path = file_path

#---------------------------- Database Methods ------------------------------
    def get_db_handler(self, user=None):
        return self.__db_handler

    def set_db_handler(self, handler, user=None):
        self.__db_handler = handler
            
#---------------------------- Access Functions ------------------------------

    # def modified_by(self, user, script_title=None):
    #     if script_title:
    #         self.__scripts[hash(script_title)]["modified_by"] = [user]

    #     self.__last_modified_by = user
    #     self.__modify_log.append(user)

    # def get_last_modified_by(self, script_title=None):
    #     if script_title:
    #         return self.__scripts[hash(script_title)]["modified_by"][-1]
    #     return self.__last_modified_by

    # def get_access(self, user):
    #     if user in self.__group or (user.access_level == self.__access_level and self.__access_level):
    #         return True
    #     return False

    # def get_group(self):
    #     return self.__group

    # def set_group(self, group):
    #     self.__group = group

    # def set_public(self, public=True):
    #     self.__public = public

    # def get_public(self):
    #     return self.__public