import pickle
import numpy
import json

from datetime import datetime
from collections import OrderedDict

from json_script import json_script

class phm_file_handler():

    @staticmethod
    def save(cluster, file_name, user=None):
        cluster.modified_by(user)
        pickle.dump( cluster, open( file_name+".phm", "wb" ) )

    @staticmethod
    def load(file_name):
        return pickle.load( open( file_name + ".phm", "rb" ) )

    def __init__(self, dbData, creator=None, group=None, access_level=None):
        
        current_date_time = datetime.now()

        self.__date_time_created = current_date_time
        self.__date_time_modified = current_date_time

        self.__dbData=dbData

        self.__creator = creator
        self.__group = group

        self.__last_modified_by = None
        self.__modify_log = []

        self.__access_level = access_level
        self.__public = True

        self.__scripts = OrderedDict()

#------------------------- script methods --------------------------
    def add_script(self, script, name, creator=None):
        if hash(name) in self.__scripts:
            print("Error: script name already exist in this ____(cluster)")
            return

        new_script = script(script, name, creator)
        self.__scripts[hash(name)]["modified_by"] = [creator]
        self.__scripts[hash(name)]["script"] = new_script

    def get_script(self, name):
        if hash(name) in self.__scripts:
            return self.__scripts[hash(name)]["script"]
        return None

    def update_script(self, name, user=None):
        if not self.__scripts[hash(name)]["script"].save_script():
            return
        self.__scripts[hash(name)]["modified_by"] = [user]

    def export_script(self, name, dest, user=None):
        json.dump(self.__scripts[hash(name)]["script"], dest)

#---------------------------- Database Methods ------------------------------
    def get_database_data(self, user=None):
        return self.__dbData
            
#---------------------------- Access Functions ------------------------------

    def modified_by(self, user, script_name=None):
        if script_name:
            self.__scripts[hash(script_name)]["modified_by"] = [user]

        self.__last_modified_by = user
        self.__modify_log.append(user)

    def get_last_modified_by(self, script_name=None):
        if script_name:
            return self.__scripts[hash(script_name)]["modified_by"][-1]
        return self.__last_modified_by

    def get_access(self, user):
        if user in self.__group or (user.access_level == self.__access_level and self.__access_level):
            return True
        return False

    def get_group(self):
        return self.__group

    def set_group(self, group):
        self.__group = group

    def set_public(self, public=True):
        self.__public = public

    def get_public(self):
        return self.__public