from datetime import datetime

class JsonScript():
    def __init__(self, script, scriptTitle=None, scriptCreator=None):

        currentDateTime = datetime.now()

        self.__dateTimeCreated = currentDateTime
        self.__dateTimeModified = currentDateTime

        self.__creator = scriptCreator
        self.__modifiedBy = scriptCreator

        self.__script = script
        self.__title = scriptTitle

    def __str__(self):
        toStr = "{"
        toStr += "\n    Created : {" 
        toStr += "\n        Date : " + str(self.__dateTimeCreated) + ","
        toStr += "\n        By : " + str(self.__creator)
        toStr += "\n    },"
        toStr += "\n    Last Modified : {"
        toStr += "\n        Date : " + str(self.__dateTimeModified) + ","
        toStr += "\n        By : " + str(self.__modifiedBy)
        toStr += "\n    },"
        toStr += "\n    Title : " + "\"" + self.__title + "\"" + ","
        toStr += "\n    Script : " + "\"" + self.__script + "\""
        toStr += "\n}"

        return toStr

    def getCreator(self):
        return self.__creator

    def getScript(self):
        return self.__script

    def setScript(self, script):
        self.__script = script

    def getDateTimeCreated(self):
        return self.__dateTimeCreated

    def getDateTimeModified(self):
        return self.__dateTimeModified

    def setModifiedBy(self, modifier):
        self.__modifiedBy = modifier

    def getModifiedBy(self):
        return self.__modifiedBy

    def setTitle(self, title):
        self.__title = title

    def getTitle(self):
        return self.__title

    def updateDateTimeModified(self):
        self.__dateTimeModified = datetime.now()
