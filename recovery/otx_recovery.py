
from logger import Logger
from recovery.base_recovery import IOCRecovery
from OTXv2 import OTXv2
from pandas.io.json import json_normalize
from formater.base_parser import Format
import requests
import time
import json
import os

OTX_KEY = "<YOUR OTX API KEY>"
OTX_GET_URL = "https://otx.alienvault.com/otxapi/pulses/{0}/export"
OTX_USR_AGT = 'OTX Python SDK/1.1'

@IOCRecovery.register
class OTXRecovery(IOCRecovery):

    def recoverIOC(self, data_path):
        logger = Logger()
        logger.info("OTXRecovery.recoverIOC")
        # Record the Starting Time
        startTime = time.time()

        dataPath = data_path + "/" + Format.OPENIOC_10.value + "/"

        # Create data dir
        if not os.path.exists(dataPath):
            os.makedirs(dataPath)

        otx = OTXv2(OTX_KEY)
        pulses = otx.getall()
        logger.info("Download complete - %s events received" % len(pulses) )

        # For each pulse get all ioc
        for pulse in pulses:
            n = json_normalize(pulse)
            url = OTX_GET_URL.format(n.id[0])
            file_name = dataPath + n.id[0] + ".ioc"

            # HTTP Request
            headers = {'X-OTX-API-KEY': OTX_KEY, 'User-Agent': OTX_USR_AGT, "Content-Type": "application/json"}
            data = {}
            params = {'format': Format.OPENIOC_10.value}
            response = requests.post(url, params=params, data=json.dumps(data), headers=headers)
            with open(file_name, "wb") as code:
                code.write(response.content)
                logger.debug("Download OpenIOC ioc file: " + n.id[0] + " - " + n["name"][0] + " -> " + file_name)

        # Trace the end time and calculate the duration
        endTime = time.time() - startTime
        logger.info('OTXRecovery finished on: ' + str(endTime) + ' seconds')