#!/bin/env python
#
# LoadAVG every 1s:   1m 5m 15m
#         Just like top but without too much info from there
#
import sys
import time

try:
    while True:
        with open('/proc/loadavg', 'r') as myfile:
            data = myfile.read().split(' ', 4)
            sys.stdout.write("\033[K{0} {1} {2}\r".format(data[0], data[1], data[2]))
        sys.stdout.flush()
        time.sleep(1)
except:
    print()
    pass
