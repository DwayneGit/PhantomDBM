import json

class default_general_settings():
    @staticmethod
    def to_str(json_dict):
        to_str = "{"
        to_str += "\n    \"db\" :  \"" + json_dict["db"] + "\","
        to_str += "\n    \"dmi\" : {" 
        to_str += "\n        \"filename\" : \"" + json_dict["dmi"]["filename"] + "\","
        to_str += "\n        \"filepath\" : \"" + json_dict["dmi"]["filepath"] + "\""
        to_str += "\n    },"
        to_str += "\n    \"login\" : {" 
        to_str += "\n        \"username\" : \"" + json_dict["login"]["username"] + "\","
        to_str += "\n        \"password\" : \"" + json_dict["login"]["password"] + "\""
        to_str += "\n    },"
        to_str += "\n    \"mongodb\" : {"
        to_str += "\n        \"dbname\" :  \"" + json_dict['mongodb']['dbname'] + "\","
        to_str += "\n        \"collection\" :  \"" + json_dict['mongodb']['collection'] + "\","
        to_str += "\n        \"host\" :  \"" + json_dict['mongodb']['host'] + "\","
        to_str += "\n        \"tableSize\" : " + str(json_dict['mongodb']['tableSize']) + ","
        to_str += "\n        \"port\" : " + str(json_dict['mongodb']['port'])
        to_str += "\n    }"
        to_str += "\n}"

        return to_str

    def __init__(self):
        self.__pref_dict = { 
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
                                    'tableSize' : 100,
                                    'port' : 27017
                                }
                    }
    
    def __str__(self):
        return default_general_settings.to_str(self.__pref_dict)

    def get_setting(self):
        return self.__pref_dict
        