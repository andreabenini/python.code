#!/usr/bin/env python3


# Python imports
import os
import sys
import logging
import argparse
import traceback
# Program imports
from ServerDaemon  import ServerDaemon
from logAdapter import logAdapter


# MAIN #
def run():
    try:
        # Environment checks
        if sys.version_info[0] < 3:
            raise Exception("Must be using Python 3")

        # Parsing input arguments
        parser = argparse.ArgumentParser(prog='service', description='Service Daemon', epilog='Service Daemon')
        parser.add_argument('action', metavar='ACTION', type=str, choices=['start', 'stop', 'restart', 'status', 'reload'],
                            help='Supported actions: start, stop, restart, status, reload')
        parser.add_argument('-l', '--loglevel', metavar='LOGLEVEL', type=str, choices=['critical', 'error', 'warning', 'info', 'debug'],
                            help='Set system log, default: info', default='info')
        args = parser.parse_args()
        DaemonName = parser.prog
        LogLevel   = args.loglevel
        Action     = args.action

        # Starting daemon
        CurrentPath = os.path.dirname(os.path.realpath(__file__))
        ServiceDaemon = ServerDaemon(name=DaemonName, basepath=CurrentPath, logLevel=LogLevel)
        # Logging setup
        logger = logAdapter(logging.getLogger(DaemonName), {'class': 'System'})

        # Processing action
        if Action == 'start':                   # Daemon start
            print("Starting %s daemon..." % DaemonName)
            logger.info('')
            logger.info('Starting service...')
            ServiceDaemon.start()
            pid = ServiceDaemon.pidGet()
            if not pid:
                print("ERROR: Cannot start %s daemon" % DaemonName)
            else:
                print("%s Daemon is running [PID:%d]" % (DaemonName, pid))

        elif Action == 'stop':                  # Daemon stop
            print("Stopping %s daemon..." % DaemonName)
            logger.info('')
            logger.info('Stopping service...')
            ServiceDaemon.stop()

        elif Action == 'restart':               # Daemon restart
            print("Restarting daemon")
            logger.info('')
            logger.info('Restarting service...')
            ServiceDaemon.restart()

        elif Action == 'reload':                # Daemon reload configuration
            print("Reloading %s configuration" % DaemonName)
            logger.info('Reloading configuration...')

        elif Action == 'status':                # Daemon status
            pid = ServiceDaemon.pidGet()
            if not pid:
                print("%s Daemon is stopped" % DaemonName)
            else:
                print("%s Daemon is running [PID:%d]" % (DaemonName, pid))
        sys.exit(0)


    except NotImplementedError as e:
        if 'logger' in locals():
            logger.error("%s    (((logger)))" % str(e))
        sys.stderr.write("\nERROR Method not implemented\n\n")
        sys.exit(1)
    except Exception as e:
        if 'logger' in locals():
            logger.error("%s    (((system)))" % str(e))
            logger.error("    %s" % (traceback.format_exc()))
        sys.stderr.write("\nERROR %s\n\n" % (str(e)))
        sys.exit(1)


if __name__ == '__main__':
    run()
