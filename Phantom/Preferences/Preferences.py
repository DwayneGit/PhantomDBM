import sys
import os.path
import json

from Phantom.ApplicationSettings import Settings

class Preferences():
    def __init__(self, configFileName, prefDict = None):
        self.configFile = configFileName + '.json'
        self.prefDict = prefDict

    def loadConfig(self):
        if (os.path.isfile(self.configFile) and
            os.stat(self.configFile).st_size != 0): #check if file exists and is not empty

            with open(self.configFile) as jsonDataFile:
                self.prefDict = json.load(jsonDataFile)
                return self.prefDict
        else:
            if not self.prefDict == None:
                self.saveConfig()
            else:
                Settings.__LOG__.logError("PREF_ERR: Preferences does not exist")

    def saveConfig( self, **kwargs ):
        """
        for key, value in kwargs.items():
            try:
                self.prefDict[key] = value
            except KeyError: 
                #Error Dialog Pop Up
        """ 
        with open(self.configFile, 'w') as outfile:
            json.dump(self.prefDict, outfile, indent=4, sort_keys=True)# save to file indent=4 & sort_keys=True make the file pretty
    