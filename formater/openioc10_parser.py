
from logger import Logger
from formater.base_parser import IOCParser, Format
import time
from xml.dom import minidom
from domain.iocdata import Evidence

@IOCParser.register
class OpenIoc10Parser(IOCParser):

    def parseEvidences(self, iocFile):
        logger = Logger()
        logger.info("OpenIoc10Parser.parseEvidence")
        # Record the Starting Time
        startTime = time.time()

        evidences_to_return = []

        # Read file
        xmldoc = minidom.parseString(iocFile)
        itemlist = xmldoc.getElementsByTagName('IndicatorItem')
        for item in itemlist:
            indicator = item.attributes['id'].value
            evidence = Evidence(indicator)
            evidences_to_return.put(evidence)

        # Trace the end time and calculate the duration
        endTime = time.time() - startTime
        logger.info('OpenIoc10Parser.parseEvidence finished on: ' + str(endTime) + ' seconds')

        return evidences_to_return

    def getFormat(self):
        return Format.OPENIOC_10