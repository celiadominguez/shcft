
from logger import Logger
from recovery.base_recovery import IOCRecovery
from formater.base_parser import Format
import base64
import requests
import time
import os
from pandas.io.json import json_normalize

XFORCE_KEY = "<YOUR XFORCE API KEY>"
XFORCE_PASS = "<YOUR XFORCE PASSWORD>"
XFORCE_GET_URL = "https://api.xforce.ibmcloud.com/casefiles/{0}/stix"
XFORCE_PUBLIC_URL = "https://api.xforce.ibmcloud.com/casefiles/public"
XFORCE_USR_AGT = 'Mozilla 5.0'

@IOCRecovery.register
class XForceRecovery(IOCRecovery):

    def recoverIOC(self, data_path):
        logger = Logger()
        logger.info("XForceRecovery.recoverIOC")
        # Record the Starting Time
        startTime = time.time()

        dataPath = data_path + "/" + Format.STIX.value + "/"

        # Create data dir
        if not os.path.exists(dataPath):
            os.makedirs(dataPath)

        # Gets all public Collections that you are able to see.
        params = {}

        author = str(base64.b64encode(bytes('%s:%s' % (XFORCE_KEY, XFORCE_PASS), 'utf-8')), 'ascii').strip()
        headers = {"Authorization": "Basic " + author,
                   "Accept": "application/json"}
        logger.info("Request - %s " % XFORCE_PUBLIC_URL )

        response = requests.get(XFORCE_PUBLIC_URL, params=params, headers=headers)

        casefiles = response.json()['casefiles'];
        logger.info("Download complete - %s events received" % len(casefiles) )

        # For each pulse get all ioc
        for casefile in casefiles:
             n = json_normalize(casefile)
             file_name = dataPath + n["caseFileID"][0] + ".ioc"

             # Get STIX file
             url = XFORCE_GET_URL.format(n["caseFileID"][0])
             response = requests.get(url, params=params, headers=headers)
             with open(file_name, "wb") as code:
                code.write(response.content)
                logger.debug("Download STIX ioc file: " + n["caseFileID"][0] + " -> " + file_name)


        # Trace the end time and calculate the duration
        endTime = time.time() - startTime
        logger.info('XForceRecovery finished on: ' + str(endTime) + ' seconds')