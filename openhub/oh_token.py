import logging

from gci.config import get_api_key

try:
    OH_TOKEN = get_api_key('OH')
except Exception as ex:
    OH_TOKEN = None
    logger = logging.getLogger(__name__)
    logger.critical('OH_TOKEN can not be obtained: %s' % ex)
