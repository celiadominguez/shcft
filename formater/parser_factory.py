
from __future__ import generators
from formater.base_parser import IOCParser


class IOCParserFactory:

    def createParser(format):
        registry = IOCParser().getRegister()
        return registry.get(format)
    createParser = staticmethod(createParser)