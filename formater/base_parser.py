
from enum import Enum

class Format(Enum):
    OPENIOC_10="openioc1.0"
    OPENIOC_11="openioc1.1"
    pass

class IOCParser(object):
    """
        Abstract class representing a ioc parser.
    """

    registry = {}
    def register(cls):
        instance = cls()
        cls.registry[instance.getFormat()] = instance
        return cls

    def getRegister(self):
        return self.registry

    pass