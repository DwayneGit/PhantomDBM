#!/usr/bin/env python

import re
import json
import copy
import pprint

import untangle

from Phantom.ApplicationSettings import Settings

class DmiHandler():
    genCounter = 0
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
        try:
            tempData = copy.deepcopy(data) # deep copy data to be manipulated
            for link in (self.root.get('link') or []):
                self.__handleLink(link, tempData)
            for gen in (self.root.get('generate') or []):
                self.__handlGen(gen, tempData)
            # pprint.pprint(tempData)
            return tempData
        except Exception as err:
            Settings.__LOG__.logError("DMI_ERR0: " + err)
            print("DMI_ERR0: " + err)

    def __handlGen(self, gen, data):
        pattern = '(\w*)({[a-z0-9:><]+})'
        if not gen.get('pattern'):
            return
        try:
            if gen.get('op') == "inc":
                pat = re.match(pattern, gen.get('pattern'))
                # print(pat[1])
                # print(pat[2])
                data[gen.get('for_field')] = pat[1] + str(pat[2].format(self.genCounter))
        except:
            pass

        self.genCounter+=1

    def __handleLink(self, link, data):
        directQueue = None
        patternQueue = None
        patternLookupKey = None
        directSearchQueue = None
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

                else:
                    if not lookup.get('filter'):
                        raise Exception("Invalid lookup")
                    directQueue = {}

            queryData['select'] = {}
            
            if link.get('select'):
                for field in link['select'].split():
                    queryData['select'][field] = 1

            elif link.get('deselect'):
                for field in link['deselect'].split():
                    queryData['select'][field] = 0

            if not patternQueue:
                for filt in (lookup.get('filter') or []):
                    temp = {}
                    temp['$and'] = []
                    temp['$and'].append(directQueue)
                    temp['$and'].append({filt['in_key'] : filt['from_key']})
                    directQueue = temp
                    # pprint.pprint(criteria)

                queryData['criteria'] = directQueue

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
