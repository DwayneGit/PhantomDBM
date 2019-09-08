#!/usr/bin/env python

import re
import json
import copy
import pprint

import untangle

from Phantom.ApplicationSettings import Settings

class DmiHandler():
    def __init__(self, dmiInstr):
        try:
            self.root = json.loads(dmiInstr)
        except Exception as err:
            Settings.__LOG__.logError("DMI_ERR: Error untangleing xml document.\n" + str(err))
            return

        self.configureInstructionSettings()

    def configureInstructionSettings(self):
        pass

    def __multipleElements(self, key):
        if isinstance(key, list):
            return True
        return False

    def manipulate(self, data):
        tempData = copy.deepcopy(data) # deep copy data to be manipulated
        for link in self.root.get('link'):
            self.__handleLink(link, tempData)
        return tempData

    def __handleLink(self, link, data):
        directQueue = None
        patternQueue = None
        patternLookupKey = None
        queryData = {}

        try:
            queryData['db_name'] = link['from_db']
        except:
            pass

        try:
            queryData['collection_name'] = link['from_collection']
        except:
            pass

        for srch in (link.get('search') or []):
            for lookup in (srch.get('look_up') or []):
                if not isinstance(lookup['from_key'], str):
                    Settings.__LOG__.logError("DMI_ERR: Value to look up is not a string")
                    return

                elif not lookup['from_key'] in data:
                    return

                # if more than one look_ups return error
                if lookup.get('method'):
                    if  lookup['method'] == "pattern":
                        patternLookupKey = lookup
                        if not lookup.get('pattern'):
                            patternQueue = list(data[lookup['from_key']])
                        else:
                            patternQueue = re.split(lookup['pattern'], lookup['from_key'])
                        # pprint.pprint(patternQueue)

                    elif lookup['method'] == "direct":
                        if not directQueue:
                            directQueue = {}
                        directQueue[lookup['in_key']] = lookup['from_key']
                        print(str(directQueue)+"57")

            queryData['select'] = {}
            
            if link.get('select'):
                for field in link['select'].split():
                    queryData['select'][field] = 1

            elif link.get('deselect'):
                for field in link['deselect'].split():
                    queryData['select'][field] = 0

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
                    if isinstance(patternLookupKey['in_key'], list):
                        criteria['$or'] = []
                        for key in patternLookupKey['in_key']:
                            temp = {}
                            point = re.split(r"\W+", key)
                            newKey = ""
                            for path in point:
                                newKey += "." + path
                            temp[newKey[1:]] = item
                            criteria['$or'].append(temp)
                    elif isinstance(patternLookupKey['in_key'], str):
                        criteria[patternLookupKey['in_key']] = item
                    else:
                        raise Exception("DMI_ERR: No in_key for lookup instruction")

                    for filt in (lookup.get('filter') or []):
                        temp = {}
                        temp['$and'] = []
                        temp['$and'].append(criteria)
                        temp['$and'].append({filt['in_key'] : filt['from_key']})
                        criteria = temp
                        # pprint.pprint(criteria)

                    if directQueue:
                        queryData['criteria'] = criteria.copy()
                        queryData['criteria'].update(directQueue)
                    else:
                        queryData['criteria'] = criteria
                        
                    self.__searchDatabase(queryData, data, link, srch)


    def __searchDatabase(self, queryData, data, link, search):
        foundDocument = Settings.__DATABASE__.findDoc(**queryData)

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
