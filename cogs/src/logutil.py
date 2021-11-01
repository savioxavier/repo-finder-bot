import logging
from .common import DEBUG

"""
        from common import USE_COLOR, DEBUG
        logging.basicConfig(
            level=logging.DEBUG if DEBUG else logging.INFO,
            format="[%(asctime)s][%(levelname)7s][%(funcName)20s][%(lineno)4s] %(message)s"
            if DEBUG
            else "[%(asctime)s][%(levelname)7s] %(message)s",
            datefmt="%I:%M.%S%p",
        )


        if USE_COLOR:
            root = logging.getLogger()
            hdlr = root.handlers[0]
            hdlr.setFormatter(CustomFormatter())

"""

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;1m"
    green = "\x1b[42;1m"
    yellow = "\x1b[43;1m"
    red = "\x1b[41;1m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    format = f"[%(asctime)s][%(levelname)-7s][%(name)-14s][%(lineno)4s] %(message)s"
    FORMATS = {
        logging.DEBUG: green + f"{reset}[%(asctime)s]{green}[%(levelname)-7s][%(name)-14s]{reset}[{red}%(lineno)4s{reset}] %(message)s" + reset,
        logging.INFO: grey + f"{reset}[%(asctime)s]{grey}[%(levelname)-7s][%(name)-14s]{reset}[{red}%(lineno)4s{reset}] %(message)s" + reset,
        logging.WARNING: yellow + f"[%(asctime)s][%(levelname)-7s][%(name)-14s][{red}%(lineno)4s{reset}{yellow}] %(message)s" + reset,
        logging.ERROR: red + f"[%(asctime)s][%(levelname)-7s][%(name)-14s][%(lineno)4s] %(message)s" + reset,
        logging.CRITICAL: bold_red + f"[%(asctime)s][%(levelname)-7s][%(name)-14s][%(lineno)4s] %(message)s" + reset
    } if DEBUG else {
        logging.DEBUG: reset,
        logging.INFO: grey + f"[%(asctime)s][%(levelname)7s] %(message)s" + reset,
        logging.WARNING: yellow + f"[%(asctime)s][%(levelname)7s] %(message)s" + reset,
        logging.ERROR: red + f"[%(asctime)s][%(levelname)7s] %(message)s" + reset,
        logging.CRITICAL: bold_red + f"[%(asctime)s][%(levelname)7s] %(message)s" + reset
    }
    # Documenting my dwindling sanity here

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%I:%M.%S%p")
        return formatter.format(record)