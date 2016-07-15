
from logger import Logger
import time

class BaseScanner(object):
    """
        Abstract class representing an evidence scanner.
    """

    registry = {}
    def register(cls):
        instance = cls()
        cls.registry[instance.getFormat()] = instance
        return cls

    def getRegister(self):
        return self.registry

    pass

    def process(self, result, **kwargs):
        pass

    def scanEvidences(self, result, **kwargs):
        path = kwargs.get("path")

        # Start scanner
        logger = Logger()
        logger.info( self.__class__ + " - Scanning %s ...  " % path)
        # Record the Starting Time
        startTime = time.time()

        self.process(self, kwargs)

        # Trace the end time and calculate the duration
        endTime = time.time() - startTime
        logger.info(self.__class__ + ' - Scanner finished on: ' + str(endTime) + ' seconds')

        return result