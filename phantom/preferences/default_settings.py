class defaultSettings():

    @staticmethod
    def toStr(jsonDict):
        toStr = "{"
        toStr += "\n    \"db\" :  \"" + jsonDict["db"] + "\","
        toStr += "\n    \"dmi\" : {"
        toStr += "\n        \"filename\" : \"" + jsonDict["dmi"]["filename"] + "\","
        toStr += "\n        \"filepath\" : \"" + jsonDict["dmi"]["filepath"] + "\""
        toStr += "\n    },"
        toStr += "\n    \"login\" : {"
        toStr += "\n        \"username\" : \"" + jsonDict["login"]["username"] + "\","
        toStr += "\n        \"password\" : \"" + jsonDict["login"]["password"] + "\""
        toStr += "\n    },"
        toStr += "\n    \"mongodb\" : {"
        toStr += "\n        \"dbname\" :  \"" + jsonDict['mongodb']['dbname'] + "\","
        toStr += "\n        \"collection\" :  \"" + jsonDict['mongodb']['collection'] + "\","
        toStr += "\n        \"host\" :  \"" + jsonDict['mongodb']['host'] + "\","
        toStr += "\n        \"port\" : " + str(jsonDict['mongodb']['port'])
        toStr += "\n    }"
        toStr += "\n}"

        return toStr

    def __init__(self):
        self.__prefDict = {
            'db' : 'mongodb',
            "dmi": {
                "filename": "",
                "filepath": ""
            },
            'login' : {
                'username' : 'Admin',
                'password' : 'Admin'
            },
            'mongodb': {
                'dbname' : '',
                'collection' : '',
                'host' : 'localhost',
                'port' : 27017
            }
        }

    def __str__(self):
        return defaultSettings.toStr(self.__prefDict)

    def getSetting(self):
        return self.__prefDict

def defaultSchemaTemplate(collection):
    default = "{\n"
    default += "\t__" + collection + " : {\n"
    default += "\t\t__schema: {\n"
    default += "\t\t}\n"
    default += "\t\t__options: {\n"
    default += "\t\tcollection: \""+ collection +"\"\n"
    default += "\t\t}\n"
    default += "\t}\n"
    default += "\t__children: {\n"
    default += "\t}\n"
    default += "}\n"
    return default        