#add option for direct db connection or api connection


import json
import pprint
from bson import ObjectId

from collections import OrderedDict
from PyQt5.QtCore import QThread

import mongoengine as mEngine
from pymongo import MongoClient
from pymongo import errors as pyErrs


from phantom.application_settings import settings

class DatabaseHandler(QThread):

    @staticmethod
    def getDatabaseList(host, port):
        client = MongoClient(host, port)
        dbn = []
        try:
            dbn = [""] + client.database_names()
        except pyErrs.ServerSelectionTimeoutError as err:
            settings.__LOG__.logError("DB_ERR: Connection refused @ " + host + ":" + str(port) + ".\n" + str(err))

        return dbn

    @staticmethod
    def getCollectionList(host, port, dbname):
        coln = []
        client = MongoClient(host=host, port=port, document_class=OrderedDict)
        try:
            db_client = client[dbname]
            coln = [""] + db_client.list_collection_names()
        except pyErrs.ServerSelectionTimeoutError as err:
            settings.__LOG__.logError("DB_ERR: Connection refused @ " + host + ":" + str(port) + " Database: " + dbname + ".\n" + str(err))
        except pyErrs.InvalidName as err:
            settings.__LOG__.logError("DB_ERR: Invalid database " + dbname +".\n" + str(err))
        return coln

    def __init__(self, db_data, authentication=None):

        self.__db_host = db_data['host']
        self.__db_name = db_data['dbname']
        self.__db_port_number = db_data['port']
        self.__db_collection = db_data['collection']

        self.__uri = "mongodb://" + self.__db_host + ":" + str(self.__db_port_number) + "/" + self.__db_name

        # self.__doc_schema_cls = None

        # self.__schema = None

        self.client = None
        self.auth = authentication

        self.dbConfig = db_data

        self.mDbDocs = []

    # def set_schema(self, schema_json, ref_schemas, db_name=None, db_coll=None):
    #     if db_name:
    #         self.__db_name = db_name
    #     if db_coll:
    #         self.__db_collection = db_coll
    #     self.__ref_schemas = ref_schemas
    #     self.__schema_json = schema_json
    #     self.__schema = schema(self.__db_collection, schema_json, ref_schemas)
    #     self.__schema.set_connection(self.__db_name, self.__db_host, self.__db_port_number)

    def get_uri(self):
        return self.__uri

    def get_collection(self):
        return self.__db_collection

    # def serverStatus(self, max_sev_sel_delay=2):
    #     if self.auth and (not self.auth.user or not self.auth.password):
    #         raise Exception("Please provide both username and password")

    #     elif self.auth and (self.auth.username and self.auth.password):
    #         try:
    #             self.client = MongoClient(host=self.__db_host, port=self.__db_port_number,
    #                                       document_class=OrderedDict, serverSelectionTimeoutMS=max_sev_sel_delay,
    #                                       username=self.auth.username, password=self.auth.password,
    #                                       authSource=self.auth.source, authMechanism=self.auth.mechanism)

    #             # The ismaster command is cheap and does not require auth.
    #             self.client.server_info()
    #             return True
    #         except pyErrs.ServerSelectionTimeoutError as err:
    #             settings.__LOG__.logError("DB_ERR: " + str(err))
    #             raise

    #     else:
    #         try:
    #             self.client = MongoClient(host=self.__db_host, port=self.__db_port_number,
    #                                       document_class=OrderedDict, serverSelectionTimeoutMS=max_sev_sel_delay)

    #             self.client.server_info()
    #             return True
    #         except pyErrs.ServerSelectionTimeoutError as err:
    #             settings.__LOG__.logError("DB_ERR: " + str(err))
    #             raise

    #     return False

    def findDoc(self, **search_data):
        settings.__LOG__.logInfo("Info to find " + str(search_data.get('criteria')))
        # pprint.pprint(search_data.get('criteria'))
        try:
            if search_data.get('db_name'):
                temp_schema = schema(search_data.get('collection_name'), self.__ref_schemas[search_data.get('collection_name')])
                temp_schema.set_connection(search_data.get('db_name'), self.__db_host, self.__db_port_number)
            elif not search_data.get('db_name') and search_data.get('collection_name'):
                temp_schema = schema(search_data.get('collection_name'), self.__ref_schemas[search_data.get('collection_name')]) #db[search_data.get('collection_name']]
                temp_schema.set_connection(self.__db_name, self.__db_host, self.__db_port_number)
            else:
                temp_schema = self.__schema

        except KeyError as err:
            settings.__LOG__.logError("SCH_ERR: No schema for collection " + str(err))
            return False

        except Exception as err:
            settings.__LOG__.logError("DMI_ERR: " + str(err))
            # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            # message = template.format(type(err).__name__, err.args)
            return False

        results = []
        try:
            for doc in temp_schema.get_schema_cls().objects(__raw__=search_data.get('criteria')):
                doc = json.loads(doc.to_json())
                doc["_id"] = ObjectId(doc["_id"]["$oid"])
                results.append(doc)

        except Exception as err:
            settings.__LOG__.logError("ERR: " + str(err))
            print(err)
            return False
            
        if len(results) > 1:
            return results
        elif len(results) == 1:
            return results[0]

        return False
        