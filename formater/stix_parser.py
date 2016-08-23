
from logger import Logger
from formater.base_parser import IOCParser, Format
from xml.dom import minidom
from domain.ioc_data import Indicator

@IOCParser.register
class STIXParser(IOCParser):

    def parseIndicator(self, iocFile, iocFileName):
        indicator_to_return = []

        # Read file
        try:
            xmldoc = minidom.parseString(iocFile)
        except Exception:
            logger = Logger()
            logger.info("Ignore IOC file {}".format(iocFile))
        else:
            itemlist = xmldoc.getElementsByTagName('stix:STIX_Package')

            for item in itemlist:
                id = item.attributes['id'].value
                title = item.getElementsByTagName('stix:Title')
                indicator = Indicator(id, self.getFormat())
                indicator.title = title
                indicator_to_return.append(indicator)

        return indicator_to_return

    @staticmethod
    def getFormat():
        return Format.STIX