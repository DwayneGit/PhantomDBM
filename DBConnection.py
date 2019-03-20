#add option for direct db connection or api connection
import re
import os
import bson
import requests

from Center import center_window
from Preferences import *
from numbers import Number

from pymongo import MongoClient
from pymongo import errors as pyErrs

from collections import OrderedDict

class APIHandler():
    def __init__(self, apiData, log):
        self.apiConfig = apiData
        self.apiName = apiData['apiname']
        self.apiRequestType = apiData['request']
        self.apiURI = apiData['uri']
        self.fLimit = apiData['tableSize']
        self.model = None
        #for docs from all collections in db#self.mDbDocs = [[0 for x in range(0)] for y in range (len(self.__db_collections))] # creates a matrix of with len(self.__db_collections) number of empty lists

        # self.mDbDocs = []
        #print(self.mDbDocs)
        self.serverStatus()

    def serverStatus(self):
        # req = requests.get(self.apiURI['base'])

        response = os.system("ping -c 1 " + self.apiURI['base'])

        #and then check the response...
        if response == 0:
            print( self.apiURI['base'], 'is up!')
            return True
        else:
            print( self.apiURI['base'], 'is down!' ) 
            return False

    def putData(self, uri, data):
        response = requests.put(uri, data)
        return response

    def postData(self, uri, data):
        response = requests.post(uri, data)
        return response

    def getData(self, uri, params=None):
        response = requests.get(uri, params)
        return response

    def deleteData(self, uri):
        response = requests.delete(uri)
        return response

class DatabaseHandler():

    @staticmethod
    def getDatabaseList(host, port):
        client = MongoClient(host, port)
        try:
            dbn = client.__db_names()
        except pyErrs.ServerSelectionTimeoutError as err:
            print("Connection refused @ " + host + ":" + str(port))
            #log err
            dbn = []
        return dbn

    @staticmethod
    def getCollectionList(host, port, dbname):
        if not dbname or dbname=="":
            return 
        client = MongoClient(host=host, port=port, document_class=OrderedDict)
        try:
            db = client[dbname]
            coln = db.list_collection_names()
        except pyErrs.ServerSelectionTimeoutError as err:
            print("Connection refused @ " + host + ":" + str(port) + " Database: " + dbname)
            #log err
            coln = []
        return coln

    def __init__(self, db_data, log, authentication=None):
        self.log = log

        self.__db_name = db_data['dbname']
        self.__db_port_number = db_data['port']
        self.__db_collection = db_data['collection']
        self.__db_host = db_data['host']
        #self.fLimit = db_data['tableSize']

        self.client = None
        self.auth = authentication

        self.dbConfig = db_data
        
        self.model = None
        # self.fSkip = findSkip
        #for docs from all collections in db#self.mDbDocs = [[0 for x in range(0)] for y in range (len(self.__db_collections))] # creates a matrix of with len(self.__db_collections) number of empty lists

        self.mDbDocs = []
        #print(self.mDbDocs)
        self.connectToDatabase()

    def get_db_name(self):
        return self.__db_name
    def get_db_port_number(self):
        return self.__db_port_number
    def get_db_collection(self):
        return self.__db_collection
    def get_db_host(self):
        return self.__db_host

    def set_db_name(self, name):
        self.__db_name = name
    def set_db_port_number(self, port_number):
        self.__db_port_number = port_number
    def set_db_collection(self, collection):
        self.__db_collection = collection
    def set_db_host(self, host):
        self.__db_host = host

    def serverStatus(self):
        max_sev_sel_delay = 2
        if self.auth and (not self.auth.user or not self.auth.password):
            print("Please provide both username and password")

        elif self.auth and (self.auth.username and self.auth.password):
            try:
                self.client = MongoClient(host=self.__db_host, port=self.__db_port_number,
                                          document_class=OrderedDict, serverSelectionTimeoutMS=max_sev_sel_delay,
                                          username=self.auth.username, password=self.auth.password,
                                          authSource=self.auth.source, authMechanism=self.auth.mechanism)

                # The ismaster command is cheap and does not require auth.
                self.client.server_info()
                return True
            except pyErrs.ServerSelectionTimeoutError as err:
                self.log.logError(err)

        else:
            try:
                self.client = MongoClient(host=self.__db_host, port=self.__db_port_number,
                                          document_class=OrderedDict, serverSelectionTimeoutMS=max_sev_sel_delay)

                # The ismaster command is cheap and does not require auth.
                self.client.server_info()
                return True
            except pyErrs.ServerSelectionTimeoutError as err:
                self.log.logError(err)
        
        return False

    def connectToDatabase(self):
        #, document_class=OrderedDict insures that the client retruns documents as ordered in database as OrderedDicts
        if not self.serverStatus():
            return

        self.collects = []

        self.db = self.client[self.__db_name]
        #print(self.db.list_collection_names())
        for col in self.db.list_collections():
            self.collects.append(col["name"])

        # if not self.__db_collection == None:
        #     docs = self.db[self.__db_collection]
        #     #print(docs)
        #     for doc in docs.find({"_id":"__Model__"}):
        #         self.model = doc
        #         #print(doc)
        #         self.mDbDocs.append(OrderedDict(self.model))

        #     for doc in docs.find(limit = self.fLimit, skip = self.fLimit*self.fSkip):
        #         #print(doc)
        #         if not doc["_id"] == "__Model__":
        #             self.mDbDocs.append(OrderedDict(doc))
        #     #print("")
        #     #print(self.mDbDocs)

    '''
    insertDoc
    inserts a document into collection
    if collection has a model it checks that the new document follows
    the model if it does it adds the doc and returns 1
    returns -1 if ther is an error or 0 if it does not follow the model
    '''
    def insertDoc(self, document):
        if not any(document.values()):
            self.errMsgs(2)
            return False
        # elif self.model:
        #     for d in document.keys():
        #         #print(document[d])
        #         #print(self.model[d])
        #         if not self.isRightType(document[d], self.model[d]) and not(d == "_id"):
        #             self.errMsgs(0)
        #             return False
        try:
            self.db[self.__db_collection].insert_one(document)
        except:
            self.errMsgs(-1)
            return False

        return True

    def findDoc(self, **search_data):
        # self.log.logInfo("Info to find " + search_data['criteria'])
        if search_data['__db_name']:
            db = self.client[search_data['__db_name']]
        else:
            db = self.db

        if search_data['collection_name']:
            docs = db[search_data['collection_name']]
        else:
            docs = db[self.__db_collection]

        results = []

        for doc in docs.find(search_data['criteria']):
            results.append(OrderedDict(doc))

        if len(results) > 1:
            return results
        elif len(results) == 1:
            return results[0]
        
        return False
        

    # def removeDoc(self, document_id):
    #     docIdQuery = dict(OrderedDict(document_id))
    #     self.db[self.__db_collection].delete_one(docIdQuery)

    # def reload(self):
    #     docs = self.db[self.__db_collection]
    #     self.mDbDocs = []
        
    #     if self.model:
    #         self.mDbDocs.append(OrderedDict(self.model))

    #     for doc in docs.find(limit = self.fLimit, skip = self.fLimit*self.fSkip):
    #         #print(doc)
    #         if not doc["_id"] == "__Model__":
    #             self.mDbDocs.append(OrderedDict(doc))

    # def createCollection(self, collectionName, data):
    #     self.db[collectionName].insert_one(data)

    # def dropCollection(self, collectionName):
    #     self.db.drop_collection(collectionName)
