
from logger import Logger
import scandir
import os
import traceback

class FileScanner():

    def __init__(self):
        pass

    registry = []
    def register(cls):
        cls.registry.append( cls() )  # Instance new subclass
        return cls

    def scanEvidences(self, indicators, path ):

        # Every type of FileScaner
        types = FileScanner.__subclasses__()
        for scanner in self.registry:
            scanner.loadEvidences(indicators)

        logger = Logger()
        logger.warn("Scanning path: %s" % path)

        # Start to scan path
        for root, directories, files in scandir.walk(path, followlinks=False):

            # Loop through files
            for filename in files:
                try:

                    # Get the file and path
                    filePath = os.path.join(root, filename)

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
                    logger.info("Error scanning file path {}: ".format(path))
                    traceback.print_exc()
                    pass
