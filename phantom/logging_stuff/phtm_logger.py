import os

import logging
import logging.config

import yaml
print(os.getcwd())
class phtm_logger():
    def __init__(self):
        with open('phantom/logging_stuff/log_config.yml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)

        self.__logger = logging.getLogger()

    def logDebug(self, message):
        self.__logger.debug(message)

    def logError(self, message):
        self.__logger.error(message)

    def logWarning(self, message):
        self.__logger.warning(message)

    def logInfo(self, message):
        self.__logger.info(message)
