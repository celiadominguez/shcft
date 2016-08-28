
from formater.base_parser import EvidenceType
from logger import Logger
from scanner.file_scanner import FileScanner


class FileNameScanner():


    def __init__(self, indicators ):
        self.evidences = {}
        self.__getEvidences__( indicators, FileNameScanner.getEvidenteType())
        pass

    @staticmethod
    def getEvidenteType():
        return EvidenceType.FILE_NAME

    def __getEvidences__(self, indicators, evidenceType):
        for indicator in indicators:
            if indicator.evidences != None:
                for evidence in indicator.evidences:
                    if evidence.type == evidenceType:
                        fileName = evidence.value
                        self.evidences[fileName.lower()] = evidence
            if indicator.children != None:
                self.__getEvidences__(indicator.children, evidenceType)

        return self.evidences

    def checkEvidences(self, filename, **kwargs):
        if filename.lower() in self.evidences:
            logger = Logger()
            logger.warn( "File Name MATCH: %s" % filename)
            evidence = self.evidences[filename]
            evidence.compromised = True


