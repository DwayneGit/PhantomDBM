import untangle
import re
import copy
from phtm_logger import phtm_logger
from DBConnection import DatabaseHandler

class DMIHandler():
    def __init__(self, db_handler, log, xml_file):
        self.log = log
        try:
            self.xml_object = untangle.parse(xml_file)
        except:
            self.log.logError("Error untangleing xml document")
            print("Error untangleing xml document")
            return
        self.db_handler = db_handler
        # self.instruction_object = {}
        self.criteria = {}
        self.root = self.xml_object.root

        self.configure_instruction_settings()

    def configure_instruction_settings(self):
        pass

    def manipulate(self, data):
        search_data = {}
        temp_data = copy.deepcopy(data) # deep copy data to be manipulated

        if self.root.from_db:
            search_data['db_name'] = self.root.from_db

        if self.root.from_collection:
            search_data['collection'] = self.root.from_collection

        for srch in self.root.link.search:

            if self.root.link['method'] == "search":
                if srch['criteria'] == "multi":
                    for lu in srch.look_up:
                        if lu['method'] == "pattern":
                            search_queue = re.split(lu['pattern'],lu.for_value)

                    self.criteria[lu.in_key] = lu.for_value
                
                else:
                    lu = srch.look_up
                    if not isinstance(lu.for_value, str):
                        print("value to look up is not a string")
                        return
                    
                    # if more than one look_ups return error
                    
                    search_queue = re.split(lu['pattern'],lu.for_value)
                    for items in search_queue:
                        
                        self.criteria[lu.in_key] = lu.items
                        search_data['criteria'] = self.criteria
                        search_data['store'] = None #<-----------------------

                        found_doc = self.db_handler.findDoc(search_data)

                        if found_doc:
                            if self.root.link['format'] == 'list':
                                if temp_data[srch['key']]:
                                    temp_data[srch['key']] = []
                                    temp_data[srch['key']].append(found_doc)
                                else:
                                    temp_data[srch['key']].append(found_doc)

                            elif self.root.link['format'] == 'auto':
                                if temp_data[srch['key']]:
                                    temp_data[srch['key']] = found_doc
                                elif temp_data[srch['key']] and not isinstance(temp_data[srch['key']], list):
                                    temp_list = []
                                    temp_list.append(temp_data[srch['key']])
                                    temp_data[srch['key']] = temp_list
                                    temp_data[srch['key']].append(found_doc)
                                else:
                                    temp_data[srch['key']].append(found_doc)

                            else:
                                temp_data[srch['key']] = found_doc

                            

