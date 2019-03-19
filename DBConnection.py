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
        #for docs from all collections in db#self.mDbDocs = [[0 for x in range(0)] for y in range (len(self.mDbCollections))] # creates a matrix of with len(self.mDbCollections) number of empty lists

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
            dbn = client.database_names()
        except pyErrs.ServerSelectionTimeoutError as err:
            print("Connection refused @ " + host + ":" + str(port))
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
            coln = []
        # print(db.list_collection_names())
        # print()
        return coln

    def __init__(self, dbData, log, authentication=None):
        self.log = log

        self.mDbName = dbData['dbname']
        self.mDbPortNum = dbData['port']
        self.mDbCollection = dbData['collection']
        self.mDbHost = dbData['host']
        self.fLimit = dbData['tableSize']

        self.client = None
        self.auth = authentication

        self.dbConfig = dbData
        
        self.model = None
        # self.fSkip = findSkip
        #for docs from all collections in db#self.mDbDocs = [[0 for x in range(0)] for y in range (len(self.mDbCollections))] # creates a matrix of with len(self.mDbCollections) number of empty lists

        self.mDbDocs = []
        #print(self.mDbDocs)
        self.connectToDatabase()

    def serverStatus(self):
        max_sev_sel_delay = 2
        if self.auth and (not self.auth.user or not self.auth.password):
            print("Please provide both username and password")

        elif self.auth and (self.auth.username and self.auth.password):
            try:
                self.client = MongoClient(host=self.mDbHost, port=self.mDbPortNum,
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
                self.client = MongoClient(host=self.mDbHost, port=self.mDbPortNum,
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

        self.db = self.client[self.mDbName]
        #print(self.db.list_collection_names())
        for col in self.db.list_collections():
            self.collects.append(col["name"])

        # if not self.mDbCollection == None:
        #     docs = self.db[self.mDbCollection]
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
            self.db[self.mDbCollection].insert_one(document)
        except:
            self.errMsgs(-1)
            return False

        return True

    # def isRightType(self, obj, tpe):
    #     #print(obj)
    #     if re.search(r"\[.*\]",tpe) and isinstance(obj,list):
    #         #elements = re.split(r",|\s,|;|\s;", obj)
    #         for ele in obj:
    #             if isinstance(ele, str):
    #                 if not re.search(r"Str",tpe):
    #                     return False
    #             elif isinstance(ele, bool): #bool is subclass of int so print first so bool wont be mistaken for ints
    #                 if not re.search(r"Bool",tpe):
    #                     return False
    #             elif isinstance(ele, (int, float)):
    #                 if not re.search(r"Num",tpe):
    #                     return False

    #         return True

    #     elif not re.search(r"\[.*\]",tpe) and isinstance(obj,list):
    #         return False

    #     else:
    #         if obj == None:
    #             return True
    #         elif isinstance(obj, str):
    #             if re.search(r"Str",tpe):
    #                 return True
    #         elif isinstance(obj, bool):
    #             if re.search(r"Bool",tpe):
    #                 return True
    #         elif isinstance(obj, (int, float)):
    #             if re.search(r"Num",tpe):
    #                 return True

    #     return False
                
    # def updateDoc(self, filt, update):
    #     if self.model:

    #         #print(next(iter(update.values())))
    #         #print(self.model[next(iter(update.keys()))])
    #         if not self.isRightType(next(iter(update.values())), self.model[next(iter(update.keys()))]) and not( next(iter(update.keys())) == "_id"):
    #             self.errMsgs(0)
    #             return False

    #     try:
    #         self.db[self.mDbCollection].update_one(filt,{'$set':update})
            
    #     except:
    #         self.errMsgs(-1)
    #         return False

    #     return True

    def findDoc(self, **search_data):
        # self.log.logInfo("Info to find " + search_data['criteria'])
        if search_data['db_name']:
            db = self.client[search_data['db_name']]
        else:
            db = self.db

        if search_data['collection_name']:
            docs = db[search_data['collection_name']]
        else:
            docs = db[self.mDbCollection]

        results = []

        # if self.model:
        #     self.mDbDocs.append(OrderedDict(self.model))

        for doc in docs.find(search_data['criteria']):
            results.append(OrderedDict(doc))

        
        # if (self.model and len(self.mDbDocs) < 2) or (not self.model and len(self.mDbDocs) < 0):
        #     self.errMsgs(3)
        #     return False
        
        if len(results) > 1:
            return results
        elif len(results) == 1:
            return results[0]
        
        return False
        

    # def removeDoc(self, document_id):
    #     docIdQuery = dict(OrderedDict(document_id))
    #     self.db[self.mDbCollection].delete_one(docIdQuery)

    # def reload(self):
    #     docs = self.db[self.mDbCollection]
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

    def errMsgs(self, code):
        msg = None
        if code == -1:
            self.log.logError('Error inserting document')
            return

        elif code == 0: msg = "One or more fields have an invalid type.\nPlease check that you have followed the model."
        elif code == 2: msg = "Entry cannot be completely empty."
        elif code == 3: msg = "No results found."
            
        errMsg = QMessageBox()
        errMsg.setText(msg)
        errMsg.setStandardButtons(QMessageBox.Ok)
        errMsg.buttonClicked.connect(errMsg.close)
        errMsg.exec_()
        return

