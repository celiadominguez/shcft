
from logger import Logger
from recovery.base_recovery import IOCRecovery
from OTXv2 import OTXv2
from pandas.io.json import json_normalize
import requests
import time
from urllib.request import build_opener, ProxyHandler, urlopen, Request
import json

OTX_KEY = "<YOUR OTX API KEY>"
OTX_GET_URL = "https://otx.alienvault.com/otxapi/pulses/{0}/export"
OTX_USR_AGT = 'OTX Python SDK/1.1'

@IOCRecovery.register
class OTXRecovery(IOCRecovery):

    def recoverIOC(self):
        logger = Logger()
        logger.info("OTXRecovery.recoverIOC")
        # Record the Starting Time
        startTime = time.time()

        otx = OTXv2(OTX_KEY)
        pulses = otx.getall()
        logger.info("Download complete - %s events received" % len(pulses) )
        for pulse in pulses:
            n = json_normalize(pulse)
            url = OTX_GET_URL.format(n.id[0])
            fileName = "./data/" + n.id[0] + ".ioc"
            logger.debug("Pulse: " + n.id[0] + " - " + n["name"][0] + " -> " + url)

            headers = {'X-OTX-API-KEY': OTX_KEY, 'User-Agent': OTX_USR_AGT, "Content-Type": "application/json"}
            data = {}
            params = {'format': 'openioc1.0'}

            response = requests.post(url, params=params, data=json.dumps(data), headers=headers)
            with open(fileName, "wb") as code:
                code.write(response.content)
                logger.debug("IOC file: " + n.id[0] + " - " + n["name"][0] + " -> " + fileName)

        # Trace the end time and calculate the duration
        endTime = time.time() - startTime
        logger.info('OTXRecovery finished on: ' + str(endTime) + ' seconds')