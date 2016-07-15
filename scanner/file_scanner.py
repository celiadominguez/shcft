
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

    for root, directories, files in scandir.walk(path, onerror=walkError, followlinks=False):

        # Loop through files
        for filename in files:
            try:

                # Get the file and path
                filePath = os.path.join(root, filename)

                # Print files
                if args.printAll:
                    print
                    "[SCANNING] %s" % filePath

                # Counter
                c += 1

                printProgress(c)

                if args.dots:
                    sys.stdout.write(".")

                file_size = os.stat(filePath).st_size
                # print file_size

                # File Name Checks -------------------------------------------------
                for file in EVIL_FILES:
                    if file in filePath:
                        print
                        Fore.RED, "\bSKELETONKEY File Name MATCH: %s" % filePath, Fore.WHITE
                        compromised = True

                # Hash Check -------------------------------------------------------
                if file_size > 200000:
                    continue

                sha1hash = sha1(filePath)
                if sha1hash in EVIL_HASHES:
                    print
                    Fore.RED, "\bSKELETON KEY SHA16 Hash MATCH: %s FILE: %s" % (sha1hash, filePath), Fore.WHITE
                    compromised = True
                if sha1hash in FALSE_POSITIVES:
                    compromised = False
                    continue

                # Yara Check -------------------------------------------------------
                if 'rules' in locals():
                    try:
                        matches = rules.match(filePath)
                        if matches:
                            for match in matches:
                                print
                                Fore.RED, "\bSKELETONKEY Yara Rule MATCH: %s FILE: %s" % (match, filePath), Fore.WHITE
                                compromised = True
                    except Exception, e:
                        if args.debug:
                            traceback.print_exc()

            except Exception, e:
                if args.debug:
                    traceback.print_exc()

    # Return result
    return compromised
pass