import sys
import os.path
import json

class Preferences():
    def __init__(self, configFileName, log, prefDict = None):
        self.log = log
        self.configFile = configFileName + '.json'
        self.prefDict = prefDict

    def loadConfig(self):
        if (os.path.isfile(self.configFile) and
            os.stat(self.configFile).st_size != 0): #check if file exists and is not empty

            with open(self.configFile) as json_data_file:
                self.prefDict = json.load(json_data_file)
                return self.prefDict
        else:
            if not self.prefDict == None:
                self.saveConfig()
            else:
                self.log.logError("Preferences does not exist")

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
    