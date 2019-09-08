#add option for direct db connection or api connection


import json
import pprint
from bson import ObjectId

from collections import OrderedDict
from PyQt5.QtCore import QThread

import mongoengine as mEngine
from pymongo import MongoClient
from pymongo import errors as pyErrs

from Phantom.ApplicationSettings import Settings

class DatabaseHandler():

    @staticmethod
    def getDatabaseList(host, port):
        client = MongoClient(host, port)
        dbn = []
        try:
            dbn = [""] + client.database_names()
        except pyErrs.ServerSelectionTimeoutError as err:
            Settings.__LOG__.logError("DB_ERR: Connection refused @ " + host + ":" + str(port) + ".\n" + str(err))
        except Exception as err:
            Settings.__LOG__.logError("ERR:" + str(err))

        return dbn

    @staticmethod
    def getCollectionList(host, port, dbname):
        coln = []
        client = MongoClient(host=host, port=port, document_class=OrderedDict)
        try:
            databaseClient = client[dbname]
            coln = [""] + databaseClient.list_collection_names()
        except pyErrs.ServerSelectionTimeoutError as err:
            Settings.__LOG__.logError("DB_ERR: Connection refused @ " + host + ":" + str(port) + " Database: " + dbname + ".\n" + str(err))
        except pyErrs.InvalidName as err:
            Settings.__LOG__.logError("DB_ERR: Invalid database " + dbname +".\n" + str(err))
        return coln

    def __init__(self, databaseData, authentication=None):

        self.__dbName = databaseData['dbname']
        self.__databaseHost = databaseData['host']
        self.__databasePortNumber = databaseData['port']
        self.__databaseCollection = databaseData['collection']

        self.__uri = "mongodb://" + self.__databaseHost + ":" + str(self.__databasePortNumber) + "/" + self.__dbName

        self.client = None
        self.auth = authentication

        self.dbConfig = databaseData

        self.mDbDocs = []

    def __str__(self):
        data = {"Database":self.__dbName, "Collection":self.__databaseCollection, "PortNumber":self.__databasePortNumber, "Host":self.__databaseHost}
        return str(data)
        
    def getHostName(self):
        return self.__databaseHost
        
    def getDatabaseName(self):
        return self.__dbName
        
    def getCollectionName(self):
        return self.__databaseCollection
        
    def getPortNumber(self):
        return self.__databasePortNumber
    
    def setHostName(self, host):
        self.__databaseHost = host
        
    def setDatabaseName(self, db):
        self.__dbName = db
        
    def setCollectionName(self, col):
        self.__databaseCollection = col
        
    def setPortNumber(self, port):
        self.__databasePortNumber = port
        
    def getUri(self):
        return self.__uri

    def getCollection(self):
        return self.__databaseCollection

    # def serverStatus(self, max_sev_sel_delay=2):
    #     if self.auth and (not self.auth.user or not self.auth.password):
    #         raise Exception("Please provide both username and password")

    #     elif self.auth and (self.auth.username and self.auth.password):
    #         try:
    #             self.client = MongoClient(host=self.__databaseHost, port=self.__databasePortNumber,
    #                                       documentClass=OrderedDict, serverSelectionTimeoutMS=max_sev_sel_delay,
    #                                       username=self.auth.username, password=self.auth.password,
    #                                       authSource=self.auth.source, authMechanism=self.auth.mechanism)

    #             # The ismaster command is cheap and does not require auth.
    #             self.client.server_info()
    #             return True
    #         except pyErrs.ServerSelectionTimeoutError as err:
    #             Settings.__LOG__.logError("DB_ERR: " + str(err))
    #             raise

    #     else:
    #         try:schema
    #             self.client = MongoClient(host=self.__databaseHost, port=self.__databasePortNumber,schema
    #                                       documentClass=OrderedDict, serverSelectionTimeoutMS=max_sev_sel_delay)schema

    #             self.client.server_info()
    #             return True
    #         except pyErrs.ServerSelectionTimeoutError as err:
    #             Settings.__LOG__.logError("DB_ERR: " + str(err))
    #             raise

    #     return False

    def findDoc(self, **queryData):
        Settings.__LOG__.logInfo("Info to find " + str(queryData.get('criteria')))
        # pprint.pprint(queryData.get('criteria'))
        try:
            if queryData.get('db_name'):
                client = MongoClient(host=self.__databaseHost, port=self.__databasePortNumber)
                try:
                    databaseClient = client[queryData.get('db_name')]
                    dbCollection = databaseClient[queryData.get('collection_name')]
                except pyErrs.ServerSelectionTimeoutError as err:
                    Settings.__LOG__.logError("DB_ERR: Connection refused @ " + host + ":" + str(port) + " Database: " + dbname + ".\n" + str(err))
                except pyErrs.InvalidName as err:
                    Settings.__LOG__.logError("DB_ERR: Invalid database " + dbname +".\n" + str(err))

            elif not queryData.get('db_name') and queryData.get('collection_name'):
                client = MongoClient(host=self.__databaseHost, port=self.__databasePortNumber)
                try:
                    databaseClient = client[self.__dbName]
                    dbCollection = databaseClient[queryData.get('collection_name')]
                except pyErrs.ServerSelectionTimeoutError as err:
                    Settings.__LOG__.logError("DB_ERR: Connection refused @ " + host + ":" + str(port) + " Database: " + dbname + ".\n" + str(err))
                except pyErrs.InvalidName as err:
                    Settings.__LOG__.logError("DB_ERR: Invalid database " + dbname +".\n" + str(err))
            else:
                raise Exception("Something Ain't Right Cheya")

        except KeyError as err:
            Settings.__LOG__.logError("SCH_ERR: No schema for collection " + str(err))
            return False

        except Exception as err:
            Settings.__LOG__.logError("DMI_ERR: " + str(err))
            # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            # message = template.format(type(err).__name__, err.args)
            return False

        results = []
        try:
            for doc in dbCollection.find(queryData.get('criteria'), queryData.get('select')):
                if not (queryData.get('select').get('_id') == 0):
                    doc["_id"] = str(doc.get("_id"))
                results.append(doc)

        except Exception as err:
            Settings.__LOG__.logError("ERR: " + str(err))
            return False
            
        if len(results) > 1:
            return results
        elif len(results) == 1:
            return results[0]

        return False
