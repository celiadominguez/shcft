import sys
import logging
from logging.handlers import RotatingFileHandler
from config import *

DEFAULT_FORMAT = "%(asctime)s %(levelname)s %(message)s"
DEFAULT_FILE_NAME = "logging.log"
DEFAULT_LOGGER_NAME = "root"
DEFAULT_NO_LOG_FILE = False
DEFAULT_LEVEL = logging.DEBUG

class Singleton(object):
    """
    Singleton interface
    """
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass

class LoggerManager(Singleton):
    """
    Logger Manager.
    Handles all logging files.
    """
    def init(self, loggerName=DEFAULT_LOGGER_NAME, logFile=DEFAULT_FILE_NAME, level=DEFAULT_LEVEL, noLogFile=DEFAULT_NO_LOG_FILE, format=DEFAULT_FORMAT):
        logging.basicConfig(filename=logFile, format=format, filemode='w')
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(level)
        rhandler = None
        try:
            rhandler = RotatingFileHandler(
                    logFile,
                    mode='a',
                    maxBytes = 10 * 1024 * 1024,
                    backupCount=5
                )
        except:
            raise IOError("Couldn't create/open file \"" + logFile + "\". Check permissions.")

    def debug(self, loggerName, msg):
        self.logger = logging.getLogger(loggerName)
        self.logger.debug(msg)

    def error(self, loggerName, msg):
        self.logger = logging.getLogger(loggerName)
        self.logger.error(msg)

    def info(self, loggerName, msg):
        self.logger = logging.getLogger(loggerName)
        self.logger.info(msg)

    def warn(self, loggerName, msg):
        self.logger = logging.getLogger(loggerName)
        self.logger.warning(msg)

class Logger(object):

    def __init__(self, loggerName=DEFAULT_LOGGER_NAME, logFile=DEFAULT_FILE_NAME, noLogFile=DEFAULT_NO_LOG_FILE, level=DEFAULT_LEVEL, format=DEFAULT_FORMAT):
        self.lm = LoggerManager(loggerName=loggerName, logFile=logFile, noLogFile=noLogFile, level=level, format=format)
        self.loggerName = loggerName
        self.logFile = logFile
        self.level = level
        self.format = format

    def debug(self, msg):
        self.lm.debug(self.loggerName, msg)

    def error(self, msg):
        self.lm.error(self.loggerName, msg)

    def info(self, msg):
        self.lm.info(self.loggerName, msg)

    def warn(self, msg):
        self.lm.warn(self.loggerName, msg)

    def print_welcome(self):
        # Record the Welcome Message
        self.info('')
        self.info('Welcome to SHCFT')
        self.info('Version' + VERSION)
        self.info('Release Date: ' + RELEASE_DATE)
        # Record some information regarding the system
        self.info('System:  ' + sys.platform)
        self.info('Version: ' + sys.version)


    def print_finish(self):
        self.info('')
        self.info('Program Terminated Normally')
