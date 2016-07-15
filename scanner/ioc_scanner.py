
"""
    Python librery to collect forensic data
    :param url: URL of the MISP instance you want to connect to
    :param out_type: Type of object (json or xml)
    :param debug: Flag to activate debug
"""

from domain.ioc_storage import *
from formater.parser_factory import IOCParserFactory
from formater.base_parser import Format
from logger import Logger
import time

class EvidenceScanner(object):

    # Constructor
    def __init__(self,  dataPath, format='json'):
        self.dataPath = dataPath
        self.format = format
        pass

    def scan(self):
        logger = Logger()
        logger.info('Start to collect evidences of compromise')
        # Record the Starting Time
        startTime = time.time()

        evidences_to_return = []

        iocDB = IocStorage(self.dataPath)
        all_iocs = iocDB.get_all_ioc(self.format)

        parser = IOCParserFactory.createParser(Format.OPENIOC_10)

        for iocFileName in all_iocs:
            logger.info("IOC file: " + iocFileName)
            iocFile = iocDB.get_ioc_file(iocFileName)
            evidences = parser.parseEvidences(iocFile)




        # Trace the end time and calculate the duration
        endTime = time.time() - startTime
        logger.info('OTXRecovery finished on: ' + str(endTime) + ' seconds')

        return evidences_to_return



