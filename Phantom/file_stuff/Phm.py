import pickle

from datetime import datetime
from collections import OrderedDict

class Phm():

    def __len__(self):
        return len(self.__scripts)

    def __init__(self, name, scripts=None, creator=None, group=None, accessLevel=None):

        self.__class__ = Phm
        self.__class__.__name__ = "Phm"

        currentDateTime = datetime.now()

        self.__name = name

        self.__dateTimeCreated = currentDateTime
        self.__dateTimeModified = currentDateTime

        self.__creator = creator
        self.__group = group

        self.__lastModifiedBy = None
        self.__modifyLog = []

        self.__accessLevel = accessLevel
        self.__public = True

        if scripts:
            self.__scripts = scripts
        else:
            self.__scripts = OrderedDict()

#---------------------------- Access Functions ------------------------------
    def getName(self):
        return self.__name
        
    def setName(self, name):
        self.__name = name

    def getScripts(self):
        return self.__scripts

    def modifiedBy(self, user, scriptTitle=None):
        if scriptTitle:
            self.__scripts[scriptTitle].setModifiedBy()

        self.__lastModifiedBy = user
        self.__modifyLog.append(user)

    def getLastModifiedBy(self, scriptTitle=None):
        if scriptTitle:
            return self.__scripts[scriptTitle].getModifiedBy()
        return self.__lastModifiedBy

    def getAccess(self, user):
        if user in self.__group or (user.accessLevel == self.__accessLevel and self.__accessLevel):
            return True
        return False

    def getGroup(self):
        return self.__group

    def setGroup(self, group):
        self.__group = group

    def isPublic(self, public):
        self.__public = public
        return self.__public

    def getTimeCreated(self):
        return self.__dateTimeCreated

    def getTimeModified(self):
        return self.__dateTimeModified

    def setTimeModified(self):
        self.__dateTimeModified = datetime.now()
