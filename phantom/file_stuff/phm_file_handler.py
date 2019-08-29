import pickle
import json
from copy import deepcopy

from PyQt5.QtWidgets import QMessageBox

from phantom.preferences import default_settings

from phantom.utility import validate_json_script

from phantom.phtm_widgets import PhtmMessageBox

from .json_script import JsonScript
from .phm import phm as phm_file

from phantom.database.database_handler import DatabaseHandler
from phantom.application_settings import settings

class PhmFileHandler():

    def __init__(self, phm=None, db_handler=None):
        self.__class__ = PhmFileHandler
        self.__class__.__name__ = "PhmFileHandler"

        self.__file_path = ""

        if phm:
            self.__phm = phm
        else:
            self.__phm = phm_file("New Cluster")
            self.add_script(str(default_settings()), "__settings__")
            self.add_script("{}", "__schema__")
            self.get_phm_scripts()["__dmi_instr__"] = {"instr" : "", "name" : "" }

        self.load_settings()
        self.__db_handler = db_handler
        self.__children = []

    def save(self, file_path, user=None):
        self.save_settings()
        tmp = deepcopy(file_path)
        if tmp[-4:] == ".phm":
            tmp = tmp[0:-4]
        pickle.dump(self.__phm, open(tmp + ".phm", "wb"))

        self.__file_path = file_path
        self.__phm.modified_by(user)

    def load(self, file_path):
        del self.__phm
        self.__phm = pickle.load(open(file_path, "rb"))
        self.load_settings()
        self.__file_path = file_path

    def load_settings(self):
        self.phm_settings = json.loads(self.get_script("__settings__").get_script())
        settings.__DATABASE__ = DatabaseHandler(self.phm_settings['mongodb'])

#------------------------- script methods --------------------------
    def add_script(self, script, title=None, creator=None):
        if title in self.get_phm_scripts():
            print(self.get_phm_scripts())
            raise Exception("Error: script title already exist in this ____(cluster)")

        try:
            validate_json_script(None, script)
            new_script = JsonScript(script, title, creator)
            self.get_phm_scripts()[title] = new_script
        except (KeyError, ValueError, json.decoder.JSONDecodeError) as err:
            err_msg = PhtmMessageBox(None, "Invalid JSON Error",
                            "Invalid JSON Format\n" + str(err))
            err_msg.exec_()
            settings.__LOG__.logError(str(err))
            raise

        return new_script

    def save_settings(self):

        self.phm_settings["mongodb"]["host"] = settings.__DATABASE__.get_host_name()
        self.phm_settings["mongodb"]["port"] = settings.__DATABASE__.get_port_number()
        self.phm_settings["mongodb"]["dbname"] = settings.__DATABASE__.get_database_name()
        self.phm_settings["mongodb"]["collection"] = settings.__DATABASE__.get_collection_name()

        sett_str = default_settings.to_str(self.phm_settings)
        self.get_script("__settings__").set_script(sett_str)

    def get_script(self, title):
        if title in self.get_phm_scripts():
            return self.get_phm_scripts()[title]
        return None

    def get_phm(self):
        return self.__phm

    def export_script(self, title, dest, user=None):
        json.dump(self.get_phm_scripts()[title], dest)

    def get_phm_scripts(self):
        return self.__phm.get_scripts()

    def get_file_path(self):
        return self.__file_path

    def set_file_path(self, file_path):
        self.__file_path = file_path

    def get_children(self):
        return self.__children

    def set_children(self, chlds):
        self.__children = chlds

#---------------------------- Database Methods ------------------------------
    def get_db_handler(self, user=None):
        return self.__db_handler

    def set_db_handler(self, handler, user=None):
        self.__db_handler = handler
