import pickle
import json
from copy import deepcopy

from PyQt5.QtWidgets import QMessageBox

from Phantom.Preferences import DefaultSettings

from Phantom.Utility import validateJsonScript

from Phantom.PhtmWidgets import PhtmMessageBox

from .JsonScript import JsonScript
from .Phm import Phm as PhmFile

from Phantom.Database.DatabaseHandler import DatabaseHandler
from Phantom.ApplicationSettings import Settings

class PhmFileHandler():

    def __init__(self, phm=None, databaseHandler=None):
        self.__class__ = PhmFileHandler
        self.__class__.__name__ = "PhmFileHandler"

        self.__filePath = ""

        if phm:
            self.__phm = phm
        else:
            self.__phm = PhmFile("New Cluster")
            self.addScript(str(DefaultSettings()), "__settings__")
            self.addScript("{}", "__schema__")
            self.getPhmScripts()["__dmi_instr__"] = {"instr" : "", "name" : "" }

        self.loadSettings()
        self.__databaseHandler = databaseHandler
        self.__children = []

    def save(self, filePath, user=None):
        self.saveSettings()
        tmp = deepcopy(filePath)
        if tmp[-4:] == ".phm":
            tmp = tmp[0:-4]
        pickle.dump(self.__phm, open(tmp + ".phm", "wb"))

        self.__filePath = filePath
        self.__phm.modifiedBy(user)

    def load(self, filePath):
        del self.__phm
        self.__phm = pickle.load(open(filePath, "rb"))
        self.loadSettings()
        self.__filePath = filePath

    def loadSettings(self):
        self.PhmSettings = json.loads(self.getScript("__settings__").getScript())
        Settings.__DATABASE__ = DatabaseHandler(self.PhmSettings['mongodb'])

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
            Settings.__LOG__.logError(str(err))
            raise

        return newScript

    def saveSettings(self):

        self.PhmSettings["mongodb"]["host"] = Settings.__DATABASE__.getHostName()
        self.PhmSettings["mongodb"]["port"] = Settings.__DATABASE__.getPortNumber()
        self.PhmSettings["mongodb"]["dbname"] = Settings.__DATABASE__.getDatabaseName()
        self.PhmSettings["mongodb"]["collection"] = Settings.__DATABASE__.getCollectionName()

        settingsStr = DefaultSettings.toStr(self.PhmSettings)
        self.getScript("__settings__").setScript(settingsStr)

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

    def setFilePath(self, filePath):
        self.__filePath = filePath

    def getChildren(self):
        return self.__children

    def setChildren(self, chlds):
        self.__children = chlds

#---------------------------- Database Methods ------------------------------
    def getDatabaseHandler(self, user=None):
        return self.__databaseHandler

    def setDatabaseHandler(self, handler, user=None):
        self.__databaseHandler = handler
