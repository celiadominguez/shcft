

from __future__ import generators
from scanner.base_scanner import BaseScanner

class EvidenceScannerFactory:

    @staticmethod
    def createScanner(id):
        registry = BaseScanner().getRegister()
        return registry.get(id)

    @staticmethod
    def scannerFactoryNames():
        types = BaseScanner.__subclasses__()
        for i in types:
            yield i.getEvidenteType()