import requests
from logger import Logger
from recovery.base_recovery import IOCRecovery
import re

IOCBUCKET_URL = "https://www.iocbucket.com/search"
IOCBUCKET_GET_URL = "https://www.iocbucket.com/iocs/{0}"

@IOCRecovery.register
class IOCBucketRecovery(IOCRecovery):
    def recoverIOC(self):
        logger = Logger()
        logger.info("IOCBucketRecovery.recoverIOC")

        response = requests.post(IOCBUCKET_URL, data={'search': 'openioc'})
        logger.debug("Result: " + response.text)

        pattern = r'<a href="/iocs/(.+)">'
        pat = re.compile(pattern)
        tuples = pat.findall(response.text)
        for iocid in tuples:
            logger.debug("Tuple: " + iocid)
            url = IOCBUCKET_GET_URL.format(iocid)
            response = requests.post(url)
            #logger.debug("Result: " + response.text)

