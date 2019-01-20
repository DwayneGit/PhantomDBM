from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from Center import center
from Preferences import *
from pymongo import MongoClient
import bson
from collections import OrderedDict
from numbers import Number
import re

class DatabaseHandler():
    def getDatabaseList( host, port):
        c = MongoClient(host, port)
        return c.database_names()

    def getCollectionList(dbData):

        client = MongoClient(host = dbData['host'], port =dbData['port'], document_class=OrderedDict)
        db = client[dbData['dbname']] 

        return db.list_collection_names()

    def __init__(self, dbData, mCollection = None, findSkip = 0):
        self.dbConfig = dbData
        self.mDbName = dbData['dbname']
        self.mDbPortNum = dbData['port']
        self.mDbCollection = mCollection
        self.mDbHost = dbData['host']
        self.fLimit = dbData['tableSize']
        self.model = None
        self.fSkip = findSkip
        #for docs from all collections in db#self.mDbDocs = [[0 for x in range(0)] for y in range (len(self.mDbCollections))] # creates a matrix of with len(self.mDbCollections) number of empty lists

        self.mDbDocs = []
        #print(self.mDbDocs)
        self.setUpDatabase()

    def setUpDatabase(self):
        #, document_class=OrderedDict insures that the client retruns documents as ordered in database as OrderedDicts
        self.client = MongoClient(host =self.mDbHost, port =self.mDbPortNum, document_class=OrderedDict)
        self.collects = []

        self.db = self.client[self.mDbName]
        #print(self.db.list_collection_names())
        for col in self.db.list_collections():
            self.collects.append(col["name"])

        if not self.mDbCollection == None:
            docs = self.db[self.mDbCollection]
            #print(docs)
            for doc in docs.find({"_id":"__Model__"}):
                self.model = doc
                #print(doc)
                self.mDbDocs.append(OrderedDict(self.model))

            for doc in docs.find(limit = self.fLimit, skip = self.fLimit*self.fSkip):
                #print(doc)
                if not doc["_id"] == "__Model__":
                    self.mDbDocs.append(OrderedDict(doc))
            #print("")
            #print(self.mDbDocs)

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
        elif self.model:
            for d in document.keys():
                #print(document[d])
                #print(self.model[d])
                if not self.isRightType(document[d], self.model[d]) and not(d == "_id"):
                    self.errMsgs(0)
                    return False
        try:
            self.db[self.mDbCollection].insert_one(document)
        except:
            self.errMsgs(-1)
            return False

        return True

    def isRightType(self, obj, tpe):
        #print(obj)
        if re.search(r"\[.*\]",tpe) and isinstance(obj,list):
            #elements = re.split(r",|\s,|;|\s;", obj)
            for ele in obj:
                if isinstance(ele, str):
                    if not re.search(r"Str",tpe):
                        return False
                elif isinstance(ele, bool): #bool is subclass of int so print first so bool wont be mistaken for ints
                    if not re.search(r"Bool",tpe):
                        return False
                elif isinstance(ele, (int, float)):
                    if not re.search(r"Num",tpe):
                        return False

            return True

        elif not re.search(r"\[.*\]",tpe) and isinstance(obj,list):
            return False

        else:
            if obj == None:
                return True
            elif isinstance(obj, str):
                if re.search(r"Str",tpe):
                    return True
            elif isinstance(obj, bool):
                if re.search(r"Bool",tpe):
                    return True
            elif isinstance(obj, (int, float)):
                if re.search(r"Num",tpe):
                    return True

        return False
                
    def updateDoc(self, filt, update):
        if self.model:

            #print(next(iter(update.values())))
            #print(self.model[next(iter(update.keys()))])
            if not self.isRightType(next(iter(update.values())), self.model[next(iter(update.keys()))]) and not( next(iter(update.keys())) == "_id"):
                self.errMsgs(0)
                return False

        try:
            self.db[self.mDbCollection].update_one(filt,{'$set':update})
            
        except:
            self.errMsgs(-1)
            return False

        return True

    def findDoc(self, findMe):
        print(findMe)
        docs = self.db[self.mDbCollection]
        self.mDbDocs = []

        if self.model:
            self.mDbDocs.append(OrderedDict(self.model))

        for doc in docs.find(findMe):
            if not doc["_id"] == "__Model__":
                self.mDbDocs.append(OrderedDict(doc))

        
        if (self.model and len(self.mDbDocs) < 2) or (not self.model and len(self.mDbDocs) < 0):
            self.errMsgs(3)
            return False
        
        return True
        

    def removeDoc(self, document_id):
        docIdQuery = dict(OrderedDict(document_id))
        self.db[self.mDbCollection].delete_one(docIdQuery)

    def reload(self):
        docs = self.db[self.mDbCollection]
        self.mDbDocs = []
        
        if self.model:
            self.mDbDocs.append(OrderedDict(self.model))

        for doc in docs.find(limit = self.fLimit, skip = self.fLimit*self.fSkip):
            #print(doc)
            if not doc["_id"] == "__Model__":
                self.mDbDocs.append(OrderedDict(doc))

    def createCollection(self, collectionName, data):
        self.db[collectionName].insert_one(data)

    def dropCollection(self, collectionName):
        self.db.drop_collection(collectionName)

    def errMsgs(self, code):
        msg = None
        if code == 0: msg ="One or more fields have an invalid type.\nPlease check that you have followed the model."
        elif code == 2: msg = "Entry cannot be completely empty."
        elif code == 3: msg = "No results found."
            
        errMsg = QMessageBox()
        errMsg.setText(msg)
        errMsg.setStandardButtons(QMessageBox.Ok)
        errMsg.buttonClicked.connect(errMsg.close)
        errMsg.exec_()
        return
        
        if code == -1:
            print('Error inserting document')
            return


