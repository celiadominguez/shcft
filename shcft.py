#
# Sherlock Holmes Computer Forensic Tools
#
# Author: C. Dominguez
#

import argparse
import logging
import sys
import time
from datetime import datetime, timezone

from analysis.ioc_analysis import IOCAnalysis
from config import *
from domain.ioc_data import AnalysisResult
from domain.ioc_handler import *
from logger import Logger
from recovery.recovery_factory import *
from report.result_report import PDFReport
from scanner.file_scanner import FileScanner

def usage():
	print ("Usage:\n\tshcft.py [first_run|check_new]")
	sys.exit(0)

# ------------ MAIN SCRIPT STARTS HERE -----------------

if __name__ == '__main__':

    # Parse Arguments
    parser = argparse.ArgumentParser(description='SHCFT - Sherlock Holmes Computer Forensic Tools')
    parser.add_argument('-d', help='Specify the root path for store Threat Intelligence', metavar='directory', default=DATA_PATH)
    parser.add_argument('-l', help='Log file', metavar='Log File', default=LOG_FILE)
    parser.add_argument('-level', help='Activate logger level for output', metavar='Log Level', default=logging.DEBUG)
    parser.add_argument('--nolog', help='Don\'t write a local log file', action='store_true', default=False)
    parser.add_argument('--norecover', help='Don\'t recover ioc files', action='store_true', default=True)
    parser.add_argument('-u', help='Your MISP\'s url', metavar='URL', default=MISP_URL)
    parser.add_argument('-k', help='The MISP auth key can be found on the MISP web interface under the automation section', metavar='MISP API key', default=MISP_KEY)

    args = parser.parse_args()
    # Record the Starting Time
    startTime = time.time()

    # Turn on Logging
    logger = Logger(logFile=args.l, noLogFile=args.nolog, level=args.level)
    logger.print_welcome()

    # Retrieves IOCs from MISP and stores them in appropriate format
    if not args.norecover:
        logger.info('Start recovering iocs from platforms')
        recoveries = [IOCRecoveryFactory.createRecovery(i)
              for i in recoveryFactoryNames()]

        for recovery in recoveries:
            recovery.recoverIOC(args.d)


    # Analyze forensic data from host system
    result = AnalysisResult( datetime.now() )

    # Get data indicators
    handler = IocHandler(args.d)
    indicators = handler.extractIndicatorOfCompromise()

    # Scan evidences
    logger.info('Start to scan evidences')
    fileScanner = FileScanner()
    fileScanner.scanEvidences(indicators, 'G:\\TFG\\TFG Celia Domínguez\\Python\\samples\\')
    # scanners = [EvidenceScannerFactory.createScanner(i)
    #           for i in EvidenceScannerFactory.scannerFactoryNames()]
    # for scanner in scanners:
    #     scanner.process(indicators)

    # Process forensic analysis of indicators
    IOCAnalysis.analyzeIndicatorsOfCompromise(indicators, result)

    # Generate a report containing detailed scan results
    report = PDFReport()
    report.generateReport(result)

    # Record the end time and calculate the duration
    endTime = time.time() - startTime
    logger.info('Elapsed Time: ' + str(endTime) + ' seconds')
    logger.info('')

    logger.print_finish()