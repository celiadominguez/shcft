import os
from exceptions import *
from logger import Logger

class IocStorage(object):

    # Constructor
    # :param format: Type of object (json or xml)
    # :param iocPath:
    def __init__(self, iocPath, format='xml'):
        if not iocPath:
            raise MissingDataPath('Please provide the root path for store data .')

        self.iocPath = iocPath
        self.format = format
        self.logger = Logger()

    def get_all_ioc(self, format='xml',):
        """
            Prepare the headers of the session
            :param format: force the type of the expect output
                          (overwrite the constructor)
        """

        out = self.format
        to_return = [];

        # Verify that the path is valid
        if os.path.exists(self.iocPath):

            # Verify that the path is not a symbolic link
            if not os.path.islink(self.iocPath):

                # Verify that the path is real
                if os.path.isdir(self.iocPath):

                    # Attempt to read the directory
                    try:
                        return os.listdir(self.iocPath)
                    except IOError:
                        raise InvalidDataPath('Path Access Error: ' + self.iocPath)
                else:
                    raise InvalidDataPath('Skipped NOT a Directory [' + self.iocPath + ']')
            else:
                raise InvalidDataPath('Skipped Link NOT a File [' + self.iocPath + ']')
        else:
            raise InvalidDataPath('Path does NOT exist [' + self.iocPath + ']')

        return to_return


    def get_ioc_file(self, iocFile):

        iocFilePath = self.iocPath + "/" + iocFile

        # Verify that the path is valid
        if os.path.exists(iocFilePath):

            # Verify that the path is not a symbolic link
            if not os.path.islink(iocFilePath):

                # Verify that the path is real
                if os.path.isfile(iocFilePath):

                    # Attempt to read the ioc file
                    try:
                        with open(iocFilePath, 'r', encoding='utf8') as myfile:
                            data = myfile.read()
                        return data
                    except IOError:
                        raise InvalidDataPath('Path Access Error: ' + iocFilePath)
                else:
                    raise InvalidDataPath('Skipped NOT a File [' + iocFilePath + ']')
            else:
                raise InvalidDataPath('Skipped Link NOT a File [' + iocFilePath + ']')
        else:
            raise InvalidDataPath('Path does NOT exist [' + iocFilePath + ']')

pass

