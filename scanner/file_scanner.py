from formater.base_parser import EvidenceType, Format
from logger import Logger
from scanner.base_scanner import BaseScanner
import scandir
import os
import traceback
from scanner.filename_scanner import FileNameScanner


@BaseScanner.register
class FileScanner(BaseScanner):
    def __init__(self):
        pass

    @staticmethod
    def getEvidenteType():
        return EvidenceType.FILE_NAME

    def process(self, indicators, **kwargs):
        path = kwargs.get("path")

        # Every type of FileScaner
        filenameScanner = FileNameScanner(indicators)
        #md5Scanner = MD5Scanner(indicators)

        path = 'G:\\TFG\\TFG Celia Domínguez\\Python\\samples\\'

        if kwargs is None or 'path' not in kwargs :
            raise TypeError("Missing keyword arguments" % 'path')

        path = kwargs['path']

        logger = Logger()
        logger.warn("Scanning path: %s" % path)

        # Start to scan path
        for root, directories, files in scandir.walk(path, followlinks=False):

            # Loop through files
            for filename in files:
                try:

                    # Get the file and path
                    filePath = os.path.join(root, filename)

                    # Print files
                    logger.debug("[SCANNING] %s" % filename)

                    # Check evidence
                    filenameScanner.checkEvidences(filename)

                except Exception:
                    logger = Logger()
                    logger.info("Error scanning file path {}: ".format(path))
                    traceback.print_exc()
                    pass
