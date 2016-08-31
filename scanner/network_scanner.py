
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

    def scanEvidences(self, indicators ):

        logger = Logger()
        logger.debug("Scanning network...")

        # Every type of NetworkScanner
        types = NetworkScanner.__subclasses__()
        for scanner in self.registry:
            scanner.loadNetworkData()
            scanner.checkEvidences(indicators)

