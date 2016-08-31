
from logger import Logger
from formater.base_parser import IOCParser, Format, EvidenceType
from xml.dom import minidom
from domain.ioc_data import Indicator, Evidence


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
                indicator = Indicator(id, self.getFormat())
                indicator.title = self.getChildrenByTagName(item, 'stix:Title')

                indicator.evidences = self.__getChildrenEvidences__(item)
                indicator_to_return.append(indicator)

        return indicator_to_return


    def getChildrenByTagName(self, node, tag_name):
        for child in node.childNodes:
            if child.nodeName == tag_name:
                if child.firstChild != None:
                    return child.firstChild.nodeValue
                else:
                    return ""
        return None

    def __getChildrenEvidences__(self, node):
        evidences_to_return = []
        itemlist = node.getElementsByTagName('cybox:Observable')
        for item in itemlist:
            evidence = Evidence()
            evidence.id = item.attributes['id'].value
            evidence.condition = 'OR'
            object = item.getElementsByTagName("cybox:Object")[0]
            property = object.getElementsByTagName("cybox:Properties")[0]
            type = property.attributes['xsi:type'].value
            self.__getEvidenceData__(object, type, evidence)

            evidences_to_return.append(evidence)

        return evidences_to_return

    def __getEvidenceData__(self, object, type, evidence):
        # File Hash value
        if type == "FileObj:FileObjectType":
            hash = object.getElementsByTagName("FileObj:Hashes")
            if hash != None:
                # Type
                hash_type = hash[0].getElementsByTagName("cyboxCommon:Type")[0]
                if hash_type.firstChild.nodeValue == "MD5":
                    evidence.type = EvidenceType.HASH_MD5
                # Value
                hash_value = object.getElementsByTagName("cyboxCommon:Simple_Hash_Value")[0]
                if hash_value.firstChild != None:
                    evidence.value = hash_value.firstChild.nodeValue
                # Context
                evidence.context = hash[0].nodeName
        # Host ip address
        elif type == "AddressObject:AddressObjectType":
            attributes = object.getElementsByTagName("cybox:Properties")[0].attributes
            if "category" in attributes:
                subtype = attributes['category'].value
                if subtype != None and subtype == "ipv4-addr":
                    evidence.type = EvidenceType.HOST
                add_value = object.getElementsByTagName("AddressObject:Address_Value")[0]
                if add_value.firstChild != None:
                    evidence.value = add_value.firstChild.nodeValue
                evidence.context = subtype

    @staticmethod
    def getFormat():
        return Format.STIX