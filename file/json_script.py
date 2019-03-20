from datetime import datetime

class json_script():
    def __init__(self, script, script_name=None, creator=None):
        
        current_date_time = datetime.now()

        self.__date_time_created = current_date_time
        self.__date_time_modified = current_date_time
        
        self.__creator = creator

        self.__script = script
        self.__script_name = script_name

    def get_script(self):
        return self.__script

    def get_creator(self):
        return self.__creator
    
    def get_date_time_created(self):
        return self.__date_time_created
    
    def get_date_time_modified(self):
        return self.__date_time_modified

    def set_script_name(self, name):
        self.__script_name = name

    def save_script(self, script):
        self.__script = script
        return True

    def update_date_time_modified(self):
        self.__date_time_modified = datetime.now()