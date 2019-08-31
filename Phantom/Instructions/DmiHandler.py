#!/usr/bin/env python

import re
import copy
import pprint

import untangle

from Phantom.ApplicationSettings import Settings

class DmiHandler():
    def __init__(self, databaseHandler, dmiInstr):
        try:
            self.xmlObject = untangle.parse(dmiInstr)
        except Exception as err:
            Settings.__LOG__.logError("DMI_ERR: Error untangleing xml document.\n" + str(err))
            return
        self.databaseHandler = databaseHandler
        self.root = self.xmlObject.root

        self.configureInstructionSettings()

    def configureInstructionSettings(self):
        pass

    def __multipleElements(self, key):
        if isinstance(key, list):
            return True
        return False

    def manipulate(self, data):
        tempData = copy.deepcopy(data) # deep copy data to be manipulated
        for link in self.root.link:
            # print("hello")
            self.__handleLink(link, tempData)
        # pprint.pprint(tempData)
        return tempData

    def __handleLink(self, link, data):
        directQueue = None
        patternQueue = None
        patternLookupKey = None
        queryData = {}

        try:
            queryData['db_name'] = link.from_db.cdata
        except:
            pass

        try:
            queryData['collection_name'] = link.from_collection.cdata
        except:
            pass

        for srch in getattr(link, 'search', []):
            for lookup in getattr(srch, 'look_up', []):
                if not isinstance(lookup.from_key.cdata, str):
                    Settings.__LOG__.logError("DMI_ERR: Value to look up is not a string")
                    return

                elif not lookup.from_key.cdata in data:
                    return

                # if more than one look_ups return error
                if lookup['method'] == "pattern":
                    patternLookupKey = lookup
                    if not lookup['pattern'] or lookup['pattern'] == "":
                        patternQueue = list(data[lookup.from_key.cdata])
                    else:
                        patternQueue = re.split(lookup['pattern'], lookup.from_key.cdata)
                    # pprint.pprint(patternQueue)

                elif lookup['method'] == "direct":
                    if not directQueue:
                        directQueue = {}
                    directQueue[lookup.in_key.cdata] = lookup.from_key.cdata
                    print(str(directQueue)+"57")

            queryData['store'] = link['store']

            if not patternQueue:
                queryData['criteria'] = directQueue
                self.__searchDatabase(queryData, data, link, srch)

            else:
                for item in patternQueue:
                    '''
                        form search critera by setting the key search in as value to find
                        if more than one keys to search in follow the formate in the following link:
                        https://stackoverflow.com/questions/8859874/pymongo-search-dict-or-operation
                    '''
                    criteria = {}
                    if isinstance(patternLookupKey.in_key, list):
                        criteria['$or'] = []
                        for key in patternLookupKey.in_key:
                            temp = {}
                            point = re.split(r"\W+", key.cdata)
                            newKey = ""
                            for path in point:
                                newKey += "." + path
                            temp[newKey[1:]] = item
                            criteria['$or'].append(temp)
                    elif isinstance(patternLookupKey.in_key, untangle.Element):
                        criteria[patternLookupKey.in_key.cdata] = item

                    for filt in getattr(lookup, 'filter', []):
                        temp = {}
                        temp['$and'] = []
                        temp['$and'].append(criteria)
                        temp['$and'].append({filt.in_key.cdata : filt.from_key.cdata})
                        criteria = temp
                        # pprint.pprint(criteria)

                    if directQueue:
                        queryData['criteria'] = criteria.copy()
                        queryData['criteria'].update(directQueue)
                    else:
                        queryData['criteria'] = criteria
                        
                    self.__searchDatabase(queryData, data, link, srch)


    def __searchDatabase(self, queryData, data, link, search):

        foundDocument = self.databaseHandler.findDoc(**queryData)

        if foundDocument:
            if link['format'] == 'list':
                if search['add_key'] not in data:
                    data[search['add_key']] = []
                    data[search['add_key']].append(foundDocument)
                else:
                    data[search['add_key']].append(foundDocument)

            elif link['format'] == 'auto':
                if search['add_key'] not in data:
                    data[search['add_key']] = foundDocument
                elif data[search['add_key']] and not isinstance(data[search['key']], list):
                    tempList = []
                    tempList.append(data[search['add_key']])
                    data[search['add_key']] = tempList
                    data[search['add_key']].append(foundDocument)
                else:
                    data[search['add_key']].append(foundDocument)

            else:
                data[search['add_key']] = foundDocument
