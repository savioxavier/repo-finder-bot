import os
import sys

from dotenv import load_dotenv

from utils import logutil

logger = logutil.init_logger("process_embed.py")

load_dotenv()


def check_for_var(varname: str):
    """
    Check if a variable is present in the environment
    """
    if varname not in os.environ:
        logger.critical(
            f"{varname} not found. Please make sure it is present in your environment variables (.env file) before starting. Terminating process..."
        )
        sys.exit(1)


def load_var(varname: str):
    """
    Load a variable from the environment
    """
    logger.info(f"Loading environment variable {varname}...")
    return str(os.environ.get(varname))


def validate_env() -> bool:
    """
    Validate environment variables
    """
    check_for_var("TOKEN")
    check_for_var("GH_TOKEN")
    check_for_var("DEV_GUILD")

    return True
