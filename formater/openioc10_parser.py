
from logger import Logger
from formater.base_parser import IOCParser, Format, EvidenceType
import time
from xml.dom import minidom
from domain.ioc_data import Indicator, Evidence
import os

@IOCParser.register
class OpenIoc10Parser(IOCParser):


    def getChildrenByTagName(self, node, tag_name):
        for child in node.childNodes:
            if child.nodeName == tag_name:
                if child.firstChild != None:
                    return child.firstChild.nodeValue
                else:
                    return ""
        return None

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
            id = os.path.splitext(iocFileName)[0]
            parent_indicator = Indicator(id, self.getFormat())
            description = self.getChildrenByTagName( xmldoc._get_firstChild(), "description")
            parent_indicator.description = description
            indicator_to_return.append(parent_indicator)

            children_indicators = []
            itemlist = xmldoc._get_firstChild().getElementsByTagName("Indicator")
            for item in itemlist:
                children_indicator = Indicator(item.attributes['id'].value, self.getFormat())
                children_indicator.operator = item.attributes['operator'].value
                children_indicator.evidences = self.__getChildrenEvidences__(item)
                children_indicator.parent = parent_indicator
                children_indicators.append(children_indicator)

            parent_indicator.children = children_indicators

        return indicator_to_return



    def __getChildrenEvidences__(self, node):
        evidences_to_return = []
        itemlist = node.getElementsByTagName('IndicatorItem')
        for item in itemlist:
            evidence = Evidence()
            evidence.id = item.attributes['id'].value
            evidence.condition = item.attributes['condition'].value
            context = item.getElementsByTagName("Context")
            if context is not None:
                evidence.context = context[0].attributes['search'].value
                evidence.type = self.__getEvidenceType__(evidence.context)
            else:
                raise ValueError("Invalid Context data")

            content = item.getElementsByTagName("Content")
            if content is not None:
                evidence.value = content[0].childNodes[0].data
            else:
                raise ValueError("Invalid Content data")

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