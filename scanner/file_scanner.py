from formater.base_parser import EvidenceType, Format
from scanner.base_scanner import BaseScanner

@BaseScanner.register
class FileScanner(BaseScanner):
    def __init__(self):
        pass

    @staticmethod
    def getEvidenteType():
        return EvidenceType.HASH_MD5

    def process(self, indicators, **kwargs):
        path = kwargs.get("path")

        evidences = self.__getEvidences__(indicators)

        pass

    def __getEvidences__(self, indicators):
        evidences_to_return = []
        return evidences_to_return


    @staticmethod
    def getEvidenceType():
        return EvidenceType.FILE_NAME