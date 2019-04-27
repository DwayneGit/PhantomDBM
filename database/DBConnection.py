#add option for direct db connection or api connection
import re
import os
import bson
import requests

from utility.center import center_window
import preferences as prefs
from numbers import Number

from pymongo import MongoClient
from pymongo import errors as pyErrs
from database.schema import schema
import mongoengine as mEngine

from collections import OrderedDict

class database_handler():

    @staticmethod
    def getDatabaseList(host, port, log):
        client = MongoClient(host, port)
        dbn = []
        try:
            dbn = [""] + client.database_names()
        except pyErrs.ServerSelectionTimeoutError as err:
            log.logError("Connection refused @ " + host + ":" + str(port))
        finally:
            return dbn

    @staticmethod
    def getCollectionList(host, port, dbname):
        coln = []
        client = MongoClient(host=host, port=port, document_class=OrderedDict)
        try:
            db = client[dbname]
            coln = [""] + db.list_collection_names()
        except pyErrs.ServerSelectionTimeoutError as err:
            print("Connection refused @ " + host + ":" + str(port) + " Database: " + dbname)
            raise err
        finally:
            return coln

    def __init__(self, db_data, log, authentication=None):
        self.log = log

        self.__db_name = db_data['dbname']
        self.__db_port_number = db_data['port']
        self.__db_collection = db_data['collection']
        self.__db_host = db_data['host']
        #self.fLimit = db_data['tableSize']

        self.__doc_schema_cls = None

        self.__schema = None
        # self.__schema.set_connection(self.__db_name)

        self.client = None
        self.auth = authentication

        self.dbConfig = db_data

        self.model = None
        # self.fSkip = findSkip
        #for docs from all collections in db#self.mDbDocs = [[0 for x in range(0)] for y in range (len(self.__db_collections))] # creates a matrix of with len(self.__db_collections) number of empty lists

        self.mDbDocs = []
        self.__connectToDatabase()

    def get_db_name(self):
        return self.__db_name
    def get_db_port_number(self):
        return self.__db_port_number
    def get_db_collection(self):
        return self.__db_collection
    def get_db_host(self):
        return self.__db_host
    def get_schema(self):
        return self.__schema

    def set_db_name(self, name):
        self.__db_name = name
    def set_db_port_number(self, port_number):
        self.__db_port_number = port_number
    def set_db_collection(self, collection):
        self.__db_collection = collection
    def set_db_host(self, host):
        self.__db_host = host
    def set_schema(self, schema_json, ref_schemas, db_name=None, db_coll=None):
        if db_name:
            self.__db_name = db_name
        if db_coll:
            self.__db_collection = db_coll
            
        self.__schema_json = schema_json
        self.__schema = schema(self.__db_name, self.__db_collection, schema_json, ref_schemas)
        self.__schema.set_connection(self.__db_name, self.__db_host, self.__db_port_number)

    def serverStatus(self, max_sev_sel_delay=2):
        if self.auth and (not self.auth.user or not self.auth.password):
            raise Exception("Please provide both username and password")

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
                self.log.logError(str(err))
                raise

        else:
            try:
                self.client = MongoClient(host=self.__db_host, port=self.__db_port_number,
                                          document_class=OrderedDict, serverSelectionTimeoutMS=max_sev_sel_delay)

                self.client.server_info()
                return True
            except pyErrs.ServerSelectionTimeoutError as err:
                self.log.logError(str(err))
                raise

        return False

    def __connectToDatabase(self):
        #, document_class=OrderedDict insures that the client retruns documents as ordered in database as OrderedDicts
        try:
            self.serverStatus()
            self.collects = []
            self.db = self.client[self.__db_name]

        except Exception as err:
            raise Exception(err)
            self.log.logError(err)

        for col in self.db.list_collections():
            self.collects.append(col["name"])

    '''
    insertDoc
    inserts a document into collection
    if collection has a model it checks that the new document follows
    the model if it does it adds the doc and returns 1
    returns -1 if ther is an error or 0 if it does not follow the model
    '''
    def insertDoc(self, document):
        new_doc = self.__schema.build_document(document)
        
        if new_doc:
            try:
                new_doc.save()
                return True
            except mEngine.ValidationError as err:
                self.log.logError(str(err))
                raise
            except mEngine.connection.MongoEngineConnectionError as err:
                self.log.logError(str(err))
                raise

    def findDoc(self, **search_data):
        self.log.logInfo("Info to find " + search_data['criteria'])
        if search_data['db_name']:
            temp_sechma = schema(search_data['db_name'], search_data['collection_name'], search_data['schema'], {})
        elif not search_data['db_name'] and search_data['collection_name']:
            temp_sechma = schema(self.__db_name, search_data['collection_name'], self.__schema_json, {}) #db[search_data['collection_name']]
        else:
            temp_sechma = self.__schema

        results = []

        for doc in temp_sechma.get_schema_cls().objects(search_data['criteria']):
            results.append(doc)

        if len(results) > 1:
            return results
        elif len(results) == 1:
            return results[0]

        return False