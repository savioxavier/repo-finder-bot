"""
Master script for the bot
"""

import os
import sys
import importlib
import inspect

import interactions

from dotenv import load_dotenv

from utils import logutil
from utils.core import get_bot_self
from utils.common import DEBUG

load_dotenv()

# Configure logging for this (main.py) handler
logger = logutil.init_logger("main.py")

logger.warning(f"Debug mode is {DEBUG}")

DEV_GUILD = int(os.environ.get("DEV_GUILD"))
TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    logger.critical("Token could not be parsed. Ensure you have a valid " +
                    "TOKEN set in your environment variables")
    sys.exit(1)

bot = interactions.Client(
    token=TOKEN,
    # presence=  # no presence yet
)


@bot.event
async def on_ready():
    bot_user = await get_bot_self()
    """Function to determine what commands are to be if bot is connected to Discord"""
    logger.info(
        f"Logged in as {bot_user.username}#{bot_user.discriminator}!")


@bot.event
async def on_command_error(ctx, error):
    logger.warning(f"A discord command error occurred:\n{error}")
    await ctx.send(f"A discord command error occurred:\n```\n{error}```\nTry your command again")

# BEGIN cogs_dynamic_loader
# Fill this array with Python files in /cogs
# This omits __init__.py, template.py, and excludes files
# without a py file extension
command_modules = [
    module[:-3]
    for module in os.listdir(f"{os.path.dirname(__file__)}/cogs")
    if module not in ("__init__.py", "template.py") and module[-3:] == ".py"
]

if command_modules or command_modules == []:
    logger.info(
        "Importing %s command modules: %s",
        len(command_modules),
        ', '.join(command_modules)
    )
else:
    logger.warning("Could not import any command modules!")

for _module in command_modules:
    try:
        _module_obj = importlib.import_module(f"cogs.{_module}")
    except Exception as e:
        logger.error(
            "Could not import command module %s:\n%s",
            _module,
            e
        )
        continue

    _cmd_module_objects = []
    for name, obj in inspect.getmembers(sys.modules[
            f"cogs.{_module}"]):
        try:
            if inspect.isclass(obj) and str(obj.__name__).upper().endswith(
                    "CMD"):
                _cmd_module_objects.append(obj)
        except Exception:  # noqa
            logger.warning("Couldn't import %s", obj.__name__)

    # init class instances in the array
    for _cmd_module in _cmd_module_objects:
        _cmd_module_inst = _cmd_module()

        try:
            # manually decorate
            bot.command(
                type=_cmd_module_inst.TYPE or interactions.ApplicationCommandType.CHAT_INPUT,
                name=_cmd_module_inst.NAME,
                description=_cmd_module_inst.DESCRIPTION or None,
                scope=DEV_GUILD or None,
                options=_cmd_module_inst.OPTIONS or None
            )(_cmd_module.command)
        except Exception:
            logger.error("Could not register %s for a command", _cmd_module.__name__, exc_info=1)
# END cogs_dynamic_loader

bot.start()
