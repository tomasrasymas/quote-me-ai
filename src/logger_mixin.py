import logging
from config import get_config
import os
from logging.handlers import RotatingFileHandler


config = get_config()


class LoggerMixin:
    def __init__(self):
        if not os.path.isdir(config.LOG_PATH):
            os.mkdir(config.LOG_PATH)

        name = '.'.join([
            self.__module__,
            self.__class__.__name__
        ])

        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s::%(name)s::%(levelname)s::%(message)s')

        file_handler = RotatingFileHandler(os.path.join(config.LOG_PATH, 'quote-me-ai.log'),
                                           maxBytes=10 * 1024 * 1024,
                                           backupCount=10)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)

        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)

    @property
    def logger(self):
        return self.__logger