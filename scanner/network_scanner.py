
from logger import Logger
import scandir
import os
import traceback

class NetworkScanner():

    def __init__(self):
        pass

    registry = []
    def register(cls):
        cls.registry.append( cls() )  # Instance new subclass
        return cls

    def scanEvidences(self, indicators, path ):

        # Every type of FileScaner
        types = NetworkScanner.__subclasses__()
        for scanner in self.registry:
            scanner.loadEvidences(indicators)

        logger = Logger()
        logger.warn("Scanning network")

