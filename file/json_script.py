from datetime import datetime

class json_script():
    def __init__(self, script, script_title=None, script_creator=None):
        
        current_date_time = datetime.now()

        self.__date_time_created = current_date_time
        self.__date_time_modified = current_date_time
        
        self.__creator = script_creator
        self.__modified_by = script_creator

        self.__script = script
        self.__title = script_title

    def __str__(self):
        to_str = "{"
        to_str += "\n    Created : {" 
        to_str += "\n        Date : " + str(self.__date_time_created) + ","
        to_str += "\n        By : " + str(self.__creator)
        to_str += "\n    },"
        to_str += "\n    Last Modified : {"
        to_str += "\n        Date : " + str(self.__date_time_modified) + ","
        to_str += "\n        By : " + str(self.__modified_by)
        to_str += "\n    },"
        to_str += "\n    Title : " + "\"" + self.__title + "\"" + ","
        to_str += "\n    Script : " + "\"" + self.__script + "\""
        to_str += "\n}"

        return to_str
        
    def get_creator(self):
        return self.__creator

    def get_script(self):
        return self.__script

    def set_script(self, script):
        self.__script = script
    
    def get_date_time_created(self):
        return self.__date_time_created
    
    def get_date_time_modified(self):
        return self.__date_time_modified

    def set_modified_by(self, modifier):
        self.__modified_by = modifier

    def get_modified_by(self):
        return self.__modified_by

    def set_title(self, title):
        self.__title = title

    def get_title(self):
        return self.__title

    def update_date_time_modified(self):
        self.__date_time_modified = datetime.now()

