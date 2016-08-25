
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
            evidence.type = self.__getEvidenceType__(object, type)
            evidence.value = self.__getEvidenceValue__(object, evidence.type)

            evidences_to_return.append(evidence)

        return evidences_to_return

    def __getEvidenceType__(self, object, type):
        if type == "FileObj:FileObjectType":
            hash = object.getElementsByTagName("FileObj:Hashes")
            if hash != None:
                hash_type = hash[0].getElementsByTagName("cyboxCommon:Type")[0]
                if hash_type.firstChild.nodeValue == "MD5":
                    return EvidenceType.HASH_MD5
        elif type == "AddressObject:AddressObjectType":
            attributes = object.getElementsByTagName("cybox:Properties")[0].attributes
            if "type" in attributes:
                subtype = attributes['type'].value
                if subtype != None and subtype == "ipv4-addr":
                    return EvidenceType.REMOTE_IP

    def __getEvidenceValue__(self, object, type):
        if type == EvidenceType.HASH_MD5:
            hash_value = object.getElementsByTagName("cyboxCommon:Simple_Hash_Value")[0]
            if hash_value.firstChild != None:
                return hash_value.firstChild.nodeValue
        elif type == EvidenceType.REMOTE_IP:
            add_value = object.getElementsByTagName("AddressObject:Address_Value")[0]
            if add_value.firstChild != None:
                return add_value.firstChild.nodeValue

    @staticmethod
    def getFormat():
        return Format.STIX