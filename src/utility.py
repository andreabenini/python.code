# Ctrl+C handler
def __SignalHandler(signal, frame):  # @UnusedVariable
    global LINE
    print('Script aborted\n')
    sys.exit(0)
# Ctrl+C signal handler in a program
import signal
signal.signal(signal.SIGINT, __SignalHandler)



import sys

# CHECK PYTHON - Check if current python version is suitable for the program
# @return (boolean) True|False if python version is fine or not
def checkPython(Version=3):
    if sys.version_info[0] >= Version:
        return True
    print("Python v{} required for this program".format(Version))
    sys.exit(1)
