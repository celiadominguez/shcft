
from enum import Enum

class Format(Enum):
    OPENIOC_10="openioc1.0"
    OPENIOC_11="openioc1.1"
    STIX="stix"

    @staticmethod
    def getFormats():
        return {Format.OPENIOC_10, Format.OPENIOC_11, Format.STIX }

    pass

class EvidenceType(Enum):
    HASH_MD5="MD5"
    HASM_SHA="SHA"
    HOST="HOST"
    REMOTE_IP="REMOTE_IP"
    FILE_NAME="FILE_NAME"

    @staticmethod
    def getTypes():
        return {EvidenceType.HASH_MD5, EvidenceType.HASM_SHA, EvidenceType.REMOTE_IP }
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