#
# Sherlock Holmes Computer Forensic Tools
#
# Author: C. Dominguez
#
# Format description
#   @variables : camelCase
#   @functions : snake_case

import logging
import sys
import time
import argparse
from logger import Logger

from config import *

from scanner.ioc_scanner import EvidenceScanner
from recovery.recovery_factory import *
from domain.iocdata import Result


def usage():
	print ("Usage:\n\tshcft.py [first_run|check_new]")
	sys.exit(0)

# ------------ MAIN SCRIPT STARTS HERE -----------------


if __name__ == '__main__':

    # Parse Arguments
    parser = argparse.ArgumentParser(description='SHCFT - Sherlock Holmes Computer Forensic Tools')
    parser.add_argument('-d', help='Specify the root path for store data', metavar='directory', default=DATA_PATH)
    parser.add_argument('-u', help='Your MISP\'s url', metavar='URL', default=MISP_URL)
    parser.add_argument('-k', help='The MISP auth key can be found on the MISP web interface under the automation section', metavar='MISP API key', default=MISP_KEY)
    parser.add_argument('-l', help='Log file', metavar='Log File', default=LOG_FILE)
    parser.add_argument('-level', help='Activate logger level for output', metavar='Log Level', default=logging.DEBUG)
    parser.add_argument('--nolog', help='Don\'t write a local log file', action='store_true', default=False)
    parser.add_argument('--norecover', help='Don\'t recover ioc files', action='store_true', default=True)

    args = parser.parse_args()
    # Record the Starting Time
    startTime = time.time()

    # Turn on Logging
    logger = Logger(logFile=args.l, noLogFile=args.nolog, level=args.level)
    logger.print_welcome()

    # Retrieves IOCs from MISP and stores them in appropriate format
    if not args.norecover:
        logger.info('Start recovering iocs from platforms')
        recoveries = [IOCRecoveryFactory.createShape(i)
              for i in recoveryFactoryNames()]

        for shape in recoveries:
            shape.recoverIOC()


    # Analyze forensic data from host system
    result = Result(time.time())

    scanner = EvidenceScanner(args.d)
    evidences = scanner.scan()

    # Process  forensic analysis of indicators
    #IndicatorAnalizer()

    # Generate a report containing detailed scan result
    #ReportGenerator()

    # Record the end time and calculate the duration
    endTime =  time.time() - startTime
    logger.info('Elapsed Time: ' + str(endTime) + ' seconds')
    logger.info('')

    logger.print_finish()