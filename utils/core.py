"""
Return core interactions attributes

"""

import os
import sys

from dotenv import load_dotenv

from utils import logutil

load_dotenv()

logger = logutil.init_logger(os.path.basename(__file__))


class RequestError(Exception):
    if str(sys.exc_info()[2]) != "None":
        logger.warning("RequestError was raised")
        logger.debug(str(sys.exc_info()[2]))
