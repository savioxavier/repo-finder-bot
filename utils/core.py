"""
Return core interactions attributes

"""

import os
import sys

import interactions
from dotenv import load_dotenv

from utils import logutil

load_dotenv()
_TOKEN = os.environ.get("TOKEN")
GH_TOKEN = str(os.environ.get("GH_TOKEN"))

# Define the client
bot = interactions.Client(token=_TOKEN)
_logger = logutil.init_logger("core.py")

if not GH_TOKEN:
    _logger.critical("Github token not found. Please make sure " +
                     "it is present in your environment variables")
    sys.exit(1)


async def get_bot_self() -> interactions.User:
    try:
        return interactions.User(**await bot.http.get_self())
    except Exception:  # noqa
        return None


class RequestError(Exception):
    if str(sys.exc_info()[2]) != "None":
        _logger.warning("RequestError was raised")
        _logger.debug(str(sys.exc_info()[2]))
