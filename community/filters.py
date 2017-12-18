import logging


class NoDebugFilter(logging.Filter):

    def filter(self, record):
        return record.levelname is not 'DEBUG'
