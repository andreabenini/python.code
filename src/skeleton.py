#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @description  TMP code to sort the queue
#
# pyright: reportMissingImports=false


# Project crap, do not keep this shit

import sys
import argparse
try:                            # These libs might not be present, checking them before importing
    import logging
except Exception as e:
    print(f"\nERROR: {str(e)}\nERROR:\nERROR: Install the required module, aborting program\n")
    sys.exit(1)
VERBOSE_LEVELS  = {'NONE':logging.CRITICAL+1, 'FULL':logging.DEBUG, 'DEBUG':logging.DEBUG, 'INFO':logging.INFO, 'WARNING':logging.WARNING, 'ERROR':logging.ERROR}
VERBOSE_DEFAULT = 'INFO'

class ApplicationLogFormatter(logging.Formatter):
    def format(self, record):
        formatter = logging.Formatter('%(asctime)s %(levelname)-7s %(filename)15s:%(lineno)-4d %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        return formatter.format(record)
class ApplicationCustomFilter():
    def __init__(self, allowed_modules):
        super().__init__()
        self.__allowedModules = allowed_modules
    def filter(self, record):
        module_name = record.name.split('.')[0]         # Get the module name from the record
        return module_name in self.__allowedModules     # Check if the module is in the list

def logInit(level):
    __logLevel = VERBOSE_LEVELS[level]
    applicationFilter = ApplicationCustomFilter('root')
    logHandler = logging.StreamHandler(stream=sys.stdout)
    logHandler.setFormatter(ApplicationLogFormatter())
    if level != 'FULL':
        logHandler.addFilter(applicationFilter)
    logging.getLogger().addHandler(logHandler)
    logging.getLogger().setLevel(__logLevel)
    logging.info("Application started")


class queueManagement():
    def __init__(self, allowed_modules):
        super().__init__()
        self.__allowedModules = allowed_modules
    def filter(self, record):
        module_name = record.name.split('.')[0]         # Get the module name from the record
        return module_name in self.__allowedModules     # Check if the module is in the list


## - - - -  MAIN  - - - -  ##
if __name__ == '__main__':
    # Input parameters
    parser = argparse.ArgumentParser(description="tmp utility", epilog=f' ', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-v', '--verbose', dest='verbose', choices=VERBOSE_LEVELS.keys(), default=VERBOSE_DEFAULT, help='Set verbosity level, default: '+VERBOSE_DEFAULT)
    arguments = parser.parse_args()
    # if not arguments.config:
    #     parser.print_help()
    #     sys.exit(1)
    # service = application.Application(configuration=arguments.config, verbose=arguments.verbose)
    # service.run()
    logInit(VERBOSE_DEFAULT)

