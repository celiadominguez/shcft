#
# Sherlock Holmes Computer Forensic Tools
#
# Author: C. Dominguez
#

import argparse
import logging
import sys
from datetime import datetime
import json
from reportlab.lib import yaml

from analysis.ioc_analysis import IOCAnalysis
from config import *
from domain.ioc_data import AnalysisResult
from domain.ioc_handler import *
from logger import Logger
from recovery.recovery_factory import *
from report.result_report import PDFReport
from scanner.file_scanner import FileScanner
from scanner.network_scanner import NetworkScanner


def usage():
	print ("Usage:\n\tshcft.py [options]")
	sys.exit(0)

# ------------ MAIN SCRIPT STARTS HERE -----------------

if __name__ == '__main__':

    # Parse Arguments
    parser = argparse.ArgumentParser(description='SHCFT - Sherlock Holmes Computer Forensic Tools')
    parser.add_argument('-d', help='Specify the root path for store Threat Intelligence', metavar='data_directory', default=DATA_PATH)
    parser.add_argument('-path', help='Specify the root path to scan on forensic analysis', metavar='path_directory', default=SCAN_PATH)
    parser.add_argument('-l', help='Log file', metavar='Log File', default=LOG_FILE)
    parser.add_argument('-level', help='Activate logger level for output', metavar='Log Level', default=logging.DEBUG)
    parser.add_argument('--nolog', help='Don\'t write a local log file', action='store_true', default=False)
    parser.add_argument('--norecover', help='Don\'t recover ioc files', action='store_true', default=False)
    parser.add_argument('-k', help="The APY KEYS used by platform receivers {['OTX_KEY': <API key>], ['XFORCE_KEY':<API_KEY>], ['XFORCE_PASS': <API_PASS>]} ", metavar='API KEYS', default='', type=str)

    args = parser.parse_args()
    # Record the Starting Time
    startTime = time.time()

    # Turn on Logging
    logger = Logger(logFile=args.l, noLogFile=args.nolog, level=args.level)
    logger.print_welcome()


    # Retrieves IOCs from platforms and stores them in appropriate format
    if not args.norecover:
        # Parsing api keys
        keys = {}
        for arg in str(args.k).split(','):
            key, val = arg.split(':')[0], arg.split(':')[1]
            keys[key] = val
        print(keys)

        # Invoke to recovery
        logger.info('Start recovering iocs from platforms')
        recoveries = [IOCRecoveryFactory.createRecovery(i)
              for i in recoveryFactoryNames()]

        for recovery in recoveries:
            recovery.recoverIOC(args.d, keys)


    # Analyze forensic data from host system
    result = AnalysisResult( datetime.now() )

    # Get data indicators
    handler = IocHandler(args.d)
    indicators = handler.extractIndicatorOfCompromise()

    # Scan evidences
    logger.info('Start to scan evidences')
    fileScanner = FileScanner()
    fileScanner.scanEvidences(indicators, args.path)

    networkScanner = NetworkScanner()
    networkScanner.scanEvidences(indicators)

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