
from formater.base_parser import EvidenceType
from logger import Logger
from scanner.file_scanner import FileScanner
import os

@FileScanner.register
class FileNameScanner(FileScanner):

    def __init__(self ):
        pass

    def loadEvidences(self, indicators ):
        self.evidences = {}
        self.__getEvidences__(indicators, FileNameScanner.getEvidenteType())
        pass

    @staticmethod
    def getEvidenteType():
        return EvidenceType.FILE_NAME

    def checkEvidences(self, filePath):
        filename = os.path.basename(filePath)
        if filename.lower() in self.evidences:
            logger = Logger()
            logger.warn( "File Name MATCH: %s" % filename)
            evidence = self.evidences[filename]
            evidence.compromised = True
            evidence.proof.append(filePath)


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
    pass