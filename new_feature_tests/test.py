import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Phantom.Database import DatabaseHandler

prefDict = {
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
        'host' : 'localhost'
        'port' : 27017
    }
}

attrs = {
    "Name" : {
        "db_field": "String",
        "required": True
    },
    "Age" : {
        "db_field": "Integer",
        "required": True,
        "max_value": 45
    }
}

test_val = DatabaseHandler(prefDict)
# test_val.generate_schema("test",attrs)