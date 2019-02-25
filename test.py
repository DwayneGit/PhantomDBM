#!/usr/bin/env python

import re
import copy
from pprint import pprint

import untangle

from phtm_logger import phtm_logger
from DBConnection import DatabaseHandler

class DMIHandler():
    def __init__(self, db_handler, xml_file, log):
        self.log = log
        try:
            self.xml_object = untangle.parse(xml_file)
        except:
            self.log.logError("Error untangleing xml document")
            print("Error untangleing xml document")
            return
        self.db_handler = db_handler
        # self.instruction_object = {}
        self.root = self.xml_object.root

        self.configure_instruction_settings()

    def configure_instruction_settings(self):
        pass

    def multiple_elements(self, key):
        if isinstance(key, list):
            return True
        return False

    def manipulate(self, data):
        # print(type(data))
        temp_data = copy.deepcopy(data) # deep copy data to be manipulated
        for link in self.root.link:
                self.__handle_link(link, temp_data)

        return temp_data

    def __handle_link(self, link, data):
        direct_queue = None
        pattern_queue = None
        pattern_lkup_key = None
        criteria = {}
        search_data = {}

        if not link.from_db :
                search_data['db_name'] = link.from_db.cdata

        if not link.from_collection:
            search_data['collection_name'] = link.from_collection.cdata

        for srch in link.search:

            for lkup in srch.look_up:
            
                if not isinstance(lkup.from_key.cdata, str):
                    print("value to look up is not a string")
                    return

                # if more than one look_ups return error
                # print(lkup['method'])
                if lkup['method'] == "pattern":
                    pattern_lkup_key = lkup
                    if not lkup['pattern'] or lkup['pattern'] == "":
                        # print(type(lkup.from_key.cdata))
                        # pprint(data)
                        # print((list(data[lkup.from_key.cdata])))
                        pattern_queue = list(data[lkup.from_key.cdata])
                    else:
                        pattern_queue = re.split(lkup['pattern'], lkup.from_key.cdata)
                    # pprint(pattern_queue)

                elif lkup['method'] == "direct":
                    if not direct_queue:
                        direct_queue = {}
                    direct_queue[lkup.in_key.cdata] = lkup.from_key.cdata
                    pprint(direct_queue)

            search_data['store'] = link['store']

            if not pattern_queue:
                search_data['criteria'] = direct_queue
                self.__search_db(search_data, data, link, srch)

            else:   
                for item in pattern_queue:
                    '''
                        form search critera by setting the key search in as value to find
                        if more than one keys to search in follow the formate in the following link:
                        https://stackoverflow.com/questions/8859874/pymongo-search-dict-or-operation
                    '''
                    # print(item)
                    # print(len(lkup.in_key))
                    if isinstance(pattern_lkup_key.in_key, list):
                        criteria['$or'] = []
                        for key in pattern_lkup_key.in_key:
                            temp={}
                            point = re.split("\W+", key.cdata)
                            new_key = ""
                            for path in point:
                                new_key += "." + path
                            temp[new_key[1:]] = item
                            criteria['$or'].append(temp)
                        # print(1)
                    elif isinstance(pattern_lkup_key.in_key, untangle.Element):
                        criteria[pattern_lkup_key.in_key.cdata] = item
                        # print(2)
                    # pprint(criteria)
                    if direct_queue:
                        search_data['criteria'] = criteria.copy()
                        search_data['criteria'].update(direct_queue)
                    else:
                        search_data['criteria'] = criteria
                    
                    self.__search_db(search_data, data, link, srch)


    def __search_db(self, search_data, data, link, search):

        # pprint(search_data)

        found_doc = self.db_handler.findDoc(**search_data)

        if found_doc:
            if link['format'] == 'list':
                if search['add_key'] not in data:
                    data[search['add_key']] = []
                    data[search['add_key']].append(found_doc)
                else:
                    data[search['add_key']].append(found_doc)

            elif link['format'] == 'auto':
                if search['add_key'] not in data:
                    data[search['add_key']] = found_doc
                elif data[search['add_key']] and not isinstance(data[search['key']], list):
                    temp_list = []
                    temp_list.append(data[search['add_key']])
                    data[search['add_key']] = temp_list
                    data[search['add_key']].append(found_doc)
                else:
                    data[search['add_key']].append(found_doc)

            else:
                data[search['add_key']] = found_doc

DATA = {
        "inKanji" : "食べる",
        "inKana" : "たべる",
        "romanji" : "taberu",
        "cls" : 1,
        "translation" : ["eat", "live on"],
        "jlptLvl" : 5,
        "pos" : "verb"
    }

xml_file = "instructions/test.xml"
# obj= untangle.parse(xml_file)

# print(len(obj.root.link))
# pattern_queue = list('たべる')
# print(pattern_queue)

dbData = {
        "collection": "jstudy",
        "dbname": "vocab",
        "host": "localhost",
        "port": 27017,
        "tableSize": 100
    }

log = phtm_logger()

db_handler = DatabaseHandler(dbData, log)
dmi = DMIHandler(db_handler, xml_file, log)

pprint(dmi.manipulate(DATA))

# point = re.split("\W+", 'dakuten->character->1')
# if len(point) > 1:
#     new_key = ""
#     for path in point:
#         new_key += "." + path
#     new_key = new_key[1:]
# print(new_key)
