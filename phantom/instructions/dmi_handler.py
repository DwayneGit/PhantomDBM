#!/usr/bin/env python

import re
import copy

import untangle

from phantom.application_settings import settings

class dmi_handler():
    def __init__(self, db_handler, dmi_instr):
        try:
            self.xml_object = untangle.parse(dmi_instr)
        except Exception as err:
            settings.__LOG__.logError("DMI_ERR: Error untangleing xml document.\n" + str(err))
            return
        self.db_handler = db_handler
        self.root = self.xml_object.root

        self.configure_instruction_settings()

    def configure_instruction_settings(self):
        pass

    def __multiple_elements(self, key):
        if isinstance(key, list):
            return True
        return False

    def manipulate(self, data):
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

        if not link.from_db:
            search_data['db_name'] = link.from_db.cdata

        if not link.from_collection:
            search_data['collection_name'] = link.from_collection.cdata

        for srch in link.search:

            for lkup in srch.look_up:

                if not isinstance(lkup.from_key.cdata, str):
                    settings.__LOG__.logError("DMI_ERR: Value to look up is not a string")
                    return

                elif not lkup.from_key.cdata in data:
                    return

                # if more than one look_ups return error
                if lkup['method'] == "pattern":
                    pattern_lkup_key = lkup
                    if not lkup['pattern'] or lkup['pattern'] == "":
                        pattern_queue = list(data[lkup.from_key.cdata])
                    else:
                        pattern_queue = re.split(lkup['pattern'], lkup.from_key.cdata)

                elif lkup['method'] == "direct":
                    if not direct_queue:
                        direct_queue = {}
                    direct_queue[lkup.in_key.cdata] = lkup.from_key.cdata

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
                    if isinstance(pattern_lkup_key.in_key, list):
                        criteria['$or'] = []
                        for key in pattern_lkup_key.in_key:
                            temp = {}
                            point = re.split(r"\W+", key.cdata)
                            new_key = ""
                            for path in point:
                                new_key += "." + path
                            temp[new_key[1:]] = item
                            criteria['$or'].append(temp)
                    elif isinstance(pattern_lkup_key.in_key, untangle.Element):
                        criteria[pattern_lkup_key.in_key.cdata] = item
                    if direct_queue:
                        search_data['criteria'] = criteria.copy()
                        search_data['criteria'].update(direct_queue)
                    else:
                        search_data['criteria'] = criteria
                    self.__search_db(search_data, data, link, srch)


    def __search_db(self, search_data, data, link, search):

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
