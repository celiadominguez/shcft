
from logger import Logger
from scanner.base_scanner import BaseScanner
import os
import time
from domain.iocdata import Result

@BaseScanner.register
class FileScanner(BaseScanner):


    def process(self, result, **kwargs):
        path = kwargs.get("path")

        return result

def scanPath(path, rules):
    # Startup
    print
    "Scanning %s ...  " % path,
    # Compromised marker
    compromised = False
    c = 0

    # Return result
    return compromised


def getFormat(self):
    return "File"

pass