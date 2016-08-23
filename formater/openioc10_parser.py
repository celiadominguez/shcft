
from logger import Logger
from formater.base_parser import IOCParser, Format, EvidenceType
import time
from xml.dom import minidom
from domain.ioc_data import Indicator, Evidence
import os

@IOCParser.register
class OpenIoc10Parser(IOCParser):

    def parseIndicator(self, iocFile, iocFileName):
        # Record the Starting Time
        startTime = time.time()

        indicator_to_return = []

        # Read file
        try:
            xmldoc = minidom.parseString(iocFile)
        except Exception:
            logger = Logger()
            logger.info("Ignore IOC file {}".format(iocFile))
        else:
            # Principal Indicator
            id = os.path.splitext(iocFileName)
            indicator = Indicator(id, self.getFormat())
            description = self.__getChildrenByTagName__( xmldoc._get_firstChild(), "description")
            indicator.description = description
            indicator_to_return.append(indicator)

            itemlist = xmldoc.getElementsByTagName('Indicator')
            for item in itemlist:
                indicator = Indicator(item.attributes['id'].value, self.getFormat())
                indicator.operator = item.attributes['operator'].value
                indicator.evidences = self.__getChildrenEvidences__(item)
                indicator_to_return.append(indicator)

        return indicator_to_return

    def __getChildrenByTagName__(self, node, tag_name):
        for child in node.childNodes:
            if child.localName == tag_name:
                yield child


    def __getChildrenEvidences__(self, node):
        evidences_to_return = []
        itemlist = node.getElementsByTagName('IndicatorItem')
        for item in itemlist:
            evidence = Evidence()
            evidence.id = item.attributes['id'].value
            evidence.condition = item.attributes['condition'].value
            evidence.content = item.getElementsByTagName("Context")[0].attributes['search'].value
            evidence.value = item.getElementsByTagName("Content")[0].data
            evidence.type = self.__getEvidenceType__(evidence.content)
            evidences_to_return.append(evidence)

        return evidences_to_return


    def __getEvidenceType__(self, search):
        if search == "FileItem/Md5sum":
            return EvidenceType.HASH_MD5
        elif search == "FileItem/Sha1sum":
            return EvidenceType.HASM_SHA
        elif search == "PortItem/remoteIP":
            return EvidenceType.REMOTE_IP
        elif search == "DnsEntryItem/Host":
            return EvidenceType.HOST

    @staticmethod
    def getFormat():
        return Format.OPENIOC_10