# Ctrl+C handler
def __SignalHandler(signal, frame):  # @UnusedVariable
    global LINE
    print('Script aborted\n')
    sys.exit(0)
# Ctrl+C signal handler in a program
import signal
signal.signal(signal.SIGINT, __SignalHandler)
