
from formater.base_parser import EvidenceType
from logger import Logger
from scanner.network_scanner import NetworkScanner
import re
import subprocess

@NetworkScanner.register
class DnsHostScanner(NetworkScanner):

    def __init__(self ):
        pass

    def loadNetworkData(self):
        self.__getDnsEntries__()
        pass

    @staticmethod
    def getEvidenteType():
        return EvidenceType.HOST

    def checkEvidences(self, indicators):
        self.evidences = []
        self.__getEvidences__(indicators, DnsHostScanner.getEvidenteType())

        for evidence in self.evidences:
            host = evidence.value
            for entry_key in self.dns_entries.keys():
                entry_value = self.dns_entries[entry_key]
                if host in entry_value:
                    logger = Logger()
                    logger.warn( "Host MATCH: %s" % host)
                    evidence.compromised = True
                    evidence.proof.append(entry_value)
                pass
        pass


    def __getEvidences__(self, indicators, evidenceType):
        for indicator in indicators:
            if indicator.evidences != None:
                for evidence in indicator.evidences:
                    if evidence.type == evidenceType:
                        self.evidences.append( evidence )

            if indicator.children != None:
                self.__getEvidences__(indicator.children, evidenceType)

        return self.evidences

    def __getDnsEntries__(self):
        self.dns_entries = {}
        output = subprocess.check_output("ipconfig /displaydns", shell=True).decode('cp1252')
        pattern = '(\s+(.*)\s+(---+))'
        regex = re.compile(pattern, re.MULTILINE)

        entry_start = None
        entry_name = None
        for match in regex.finditer(output):
            # print ("[%s]: %s" % (match.start(), match.group(2)))
            if entry_start != None:
                self.dns_entries[entry_name] = output[entry_start:match.start()].strip()
            entry_name = match.group(2)
            entry_start = match.start()
        pass