import traceback

from formater.base_parser import EvidenceType
from logger import Logger
import hashlib
from scanner.file_scanner import FileScanner

@FileScanner.register
class MD5Scanner(FileScanner):

    def __init__(self ):
        pass

    def loadEvidences(self, indicators ):
        self.evidences = {}
        self.__getEvidences__(indicators, MD5Scanner.getEvidenteType())
        pass

    @staticmethod
    def getEvidenteType():
        return EvidenceType.HASH_MD5

    def checkEvidences(self, filePath):

        # Calculate the MD5
        try:
            with open(filePath, 'rb') as file:
                file_data = file.read()
            hashValue = hashlib.md5(file_data).hexdigest()
            logger = Logger()
            logger.warn(("Hash file {}: {}").format( filePath, hashValue) )

            if hashValue in self.evidences:
                logger = Logger()
                logger.warn("Hash md5 MATCH: %s" % filePath)
                evidence = self.evidences[hashValue]
                evidence.compromised = True
                evidence.proof.append(filePath)

        except Exception:
            traceback.print_exc()
        pass

    def __getEvidences__(self, indicators, evidenceType):
        for indicator in indicators:
            if indicator.evidences != None:
                for evidence in indicator.evidences:
                    if evidence.type == evidenceType:
                        self.evidences[evidence.value] = evidence
            if indicator.children != None:
                self.__getEvidences__(indicator.children, evidenceType)
        return self.evidences

    pass