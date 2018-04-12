import logging

from gci.config import get_api_key

try:
    GH_TOKEN = get_api_key('GH')
except Exception as ex:
    GH_TOKEN = None
    logger = logging.getLogger(__name__)
    logger.critical('GH_TOKEN can not be obtained: %s' % ex)
