# Python imports
import logging


# Custom log adapter class
class logAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return '%-12s %s' % (self.extra['class'], msg), kwargs
