# Custom logging with attributes inherited, custom prints for each single class
# @see:  Python website is your best friend even if logging doc is a mess
#        - https://docs.python.org/3/howto/logging.html
#        - https://docs.python.org/3/howto/logging-cookbook.html
import logging

def LoggerSetup():
    logger = logging.getLogger("Something")
    logger.setLevel(logging.DEBUG)
    Formatter   = logging.Formatter('%(asctime)-15s [%(levelname)-8s] %(message)s', '%Y-%m-%d %H:%M:%S')
    FileHandler = logging.FileHandler('/tmp/log.log')
    FileHandler.setFormatter(Formatter)
    logger.addHandler(FileHandler)
    logger.info("")
    logger.info("Log Started")

class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return '%-12s %s' % (self.extra['class'], msg), kwargs

class BaseClass():
    def __init__(self):
        self.name   = self.__class__.__name__
        self.logger = CustomAdapter(logging.getLogger('Something'), {'class': self.name})
        # was: self.logger = logging.getLogger("Something")
        self.logger.info("inherited log")


class DerivedClass(BaseClass):
    def __init__(self):
        super(DerivedClass, self).__init__()
        self.logger.info("[Derived] rules now !")

LoggerSetup()
B = BaseClass()
D = DerivedClass()



# Debug, quick and dirty for tests, useful for a 5min debug on simple scripts
logging.basicConfig(filename='/tmp/debug.log', level=logging.DEBUG)
logging.debug("Something to write in the log file")
