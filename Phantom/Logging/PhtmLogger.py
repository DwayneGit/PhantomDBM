import os

import logging
import logging.config

import yaml

class PhtmLogger():
    def __init__(self):
        with open('Phantom/Logging/log_config.yml', 'r') as f:
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
