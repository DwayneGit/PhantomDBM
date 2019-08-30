import pickle
import json
from copy import deepcopy

from PyQt5.QtWidgets import QMessageBox

from phantom.preferences import default_settings

from phantom.utility import validateJsonScript

from phantom.phtmWidgets import PhtmMessageBox

from .json_script import JsonScript
from .phm import phm as phm_file

from phantom.database.database_handler import DatabaseHandler
from phantom.applicationSettings import settings

class PhmFileHandler():

    def __init__(self, phm=None, db_handler=None):
        self.__class__ = PhmFileHandler
        self.__class__.__name__ = "PhmFileHandler"

        self.__filePath = ""

        if phm:
            self.__phm = phm
        else:
            self.__phm = phm_file("New Cluster")
            self.addScript(str(default_settings()), "__settings__")
            self.addScript("{}", "__schema__")
            self.getPhmScripts()["__dmi_instr__"] = {"instr" : "", "name" : "" }

        self.load_settings()
        self.__db_handler = db_handler
        self.__children = []

    def save(self, filePath, user=None):
        self.save_settings()
        tmp = deepcopy(filePath)
        if tmp[-4:] == ".phm":
            tmp = tmp[0:-4]
        pickle.dump(self.__phm, open(tmp + ".phm", "wb"))

        self.__filePath = filePath
        self.__phm.modified_by(user)

    def load(self, filePath):
        del self.__phm
        self.__phm = pickle.load(open(filePath, "rb"))
        self.load_settings()
        self.__filePath = filePath

    def load_settings(self):
        self.phm_settings = json.loads(self.getScript("__settings__").getScript())
        settings.__DATABASE__ = DatabaseHandler(self.phm_settings['mongodb'])

#------------------------- script methods --------------------------
    def addScript(self, script, title=None, creator=None):
        if title in self.getPhmScripts():
            print(self.getPhmScripts())
            raise Exception("Error: script title already exist in this ____(cluster)")

        try:
            validateJsonScript(None, script)
            newScript = JsonScript(script, title, creator)
            self.getPhmScripts()[title] = newScript
        except (KeyError, ValueError, json.decoder.JSONDecodeError) as err:
            errorMessage = PhtmMessageBox(None, "Invalid JSON Error",
                            "Invalid JSON Format\n" + str(err))
            errorMessage.exec_()
            settings.__LOG__.logError(str(err))
            raise

        return newScript

    def save_settings(self):

        self.phm_settings["mongodb"]["host"] = settings.__DATABASE__.getHostName()
        self.phm_settings["mongodb"]["port"] = settings.__DATABASE__.getPortNumber()
        self.phm_settings["mongodb"]["dbname"] = settings.__DATABASE__.getDatabaseName()
        self.phm_settings["mongodb"]["collection"] = settings.__DATABASE__.getCollectionName()

        sett_str = default_settings.to_str(self.phm_settings)
        self.getScript("__settings__").set_script(sett_str)

    def getScript(self, title):
        if title in self.getPhmScripts():
            return self.getPhmScripts()[title]
        return None

    def getPhm(self):
        return self.__phm

    def exportScript(self, title, dest, user=None):
        json.dump(self.getPhmScripts()[title], dest)

    def getPhmScripts(self):
        return self.__phm.getScripts()

    def getFilePath(self):
        return self.__filePath

    def set_filePath(self, filePath):
        self.__filePath = filePath

    def get_children(self):
        return self.__children

    def set_children(self, chlds):
        self.__children = chlds

#---------------------------- Database Methods ------------------------------
    def get_db_handler(self, user=None):
        return self.__db_handler

    def set_db_handler(self, handler, user=None):
        self.__db_handler = handler
