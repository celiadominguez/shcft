from urllib.parse import urlencode

from logger import Logger
import scandir
import os
import traceback

try:
    from os import scandir
except ImportError:
    from scandir import scandir  # use scandir PyPI module on Python < 3.5

def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  # see below for Python 2.x
        else:
            yield entry

class FileScanner():

    def __init__(self):
        pass

    registry = []
    def register(cls):
        cls.registry.append( cls() )  # Instance new subclass
        return cls


    def scanEvidences(self, indicators, path='.' ):

        # Every type of FileScaner
        types = FileScanner.__subclasses__()
        for scanner in self.registry:
            scanner.loadEvidences(indicators)

        logger = Logger()
        logger.debug("Scanning path: %s" % path)

        #path = urlencode(path)

        # Start to scan path
        for entry in scantree(path):
            #print(entry.path)
            #for root, directories, files in scandir.walk(entry.path, followlinks=False):

        # Loop through files
        #for filename in files:
            try:

                # Get the file and path
                #filePath = os.path.join(root, filename)
                filePath = entry.path
                # Verify that the path is valid
                if os.path.exists(filePath):

                    # Verify that the path is not a symbolic link
                    if not os.path.islink(filePath):

                        # Verify that the file is real
                        if os.path.isfile(filePath):

                            # Print files
                            logger.debug("[SCANNING] %s" % filePath)

                            # Check evidence
                            for scanner in self.registry:
                                scanner.checkEvidences(filePath)

            except Exception:
                logger = Logger()
                logger.warn("Error scanning file path {}: ".format(entry.path))
                traceback.print_exc()
                pass
