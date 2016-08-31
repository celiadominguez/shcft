import os
from exceptions import *
from formater.base_parser import Format
from formater.parser_factory import IOCParserFactory
from logger import Logger
import time

class IocHandler(object):

    # Constructor
    # :param format: Type of object (json or xml)
    # :param iocPath:
    def __init__(self, ioc_path, format='xml'):
        if not ioc_path:
            raise MissingDataPath('Please provide the root path for store data .')

        self.data_path = ioc_path
        self.format = format
        self.logger = Logger()

    def get_all_ioc(self, format='xml'):
        """
            Prepare the headers of the session
            :param format: force the type of the expect output
                          (overwrite the constructor)
        """

        out = self.format
        to_return = [];

        # Verify that the path is valid
        if os.path.exists(self.data_path):

            # Verify that the path is not a symbolic link
            if not os.path.islink(self.data_path):

                # Verify that the path is real
                if os.path.isdir(self.data_path):

                    # Attempt to read the directory
                    try:
                        return os.listdir(self.data_path)
                    except IOError:
                        raise InvalidDataPath('Path Access Error: ' + self.data_path)
                else:
                    raise InvalidDataPath('Skipped NOT a Directory [' + self.data_path + ']')
            else:
                raise InvalidDataPath('Skipped Link NOT a File [' + self.data_path + ']')
        else:
            raise InvalidDataPath('Path does NOT exist [' + self.data_path + ']')

        return to_return


    def get_ioc_file(self, iocFile):

        iocFilePath = self.data_path + "/" + iocFile

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


    def extractIndicatorOfCompromise(self):
        logger = Logger()
        logger.info('Start to extract indicator of compromise from data repository: {}'.format(self.data_path))
        # Record the Starting Time
        startTime = time.time()

        indicators_to_return = []

        formats = Format.getFormats()
        for format in formats:
            iocDB = IocHandler(self.data_path + "/" + format.value + "/")
            try:
                all_iocs = iocDB.get_all_ioc(format)

            except InvalidDataPath:
                logger.info("Ignore IOC format {}".format(format.value))
                continue


            logger.info("Getting IOC files with format: " + format.value)
            parser = IOCParserFactory.createParser(format)

            for iocFileName in all_iocs:
                iocFile = iocDB.get_ioc_file(iocFileName)
                indicators = parser.parseIndicator(iocFile, iocFileName)
                indicators_to_return = indicators_to_return + indicators

        # Trace the end time and calculate the duration
        endTime = time.time() - startTime
        logger.info('Extract ({}) IOCs finished on: {} seconds'.format(indicators_to_return.__len__(), str(endTime)))

        return indicators_to_return
pass

