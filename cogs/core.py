"""
Repo Finder command script for the bot
"""

import os
import sys

from discord.ext import commands
from discord.ext.commands import Cog

from cogs.src import logutil

logger = logutil.initLogger("core.py")

DEV_GUILD = int(os.environ.get("DEV_GUILD"))
GH_TOKEN = str(os.environ.get("GH_TOKEN"))

__GUILD_IDS__ = [DEV_GUILD]


class RequestError(Exception):
    # Will discord_error throw any tracebacks?
    if str(sys.exc_info()[2]) != "None":
        # Edit: ok I googled it. Yes it does
        logger.warning("RequestError was raised")
        # Edit 2: Is this code even good? Probably not, but it prevents it from being called on script boot
        logger.debug(str(sys.exc_info()[2]))
    pass


# dynamically load all cogs found in commands as modules
# prepare for slash_commands
command_modules = []
try:
    # os.chdir(os.path.dirname(__file__) + "/src/commands")
    sys.path.insert(0, os.path.dirname(__file__) + "/src/commands")
    for module in os.listdir(f"{os.path.dirname(__file__)}/src/commands"):
        try:
            if module in ("__init__.py", "template.py") or module[-3:] != ".py":
                continue
            __import__("cogs.src.commands." + module[:-3], locals(), globals())
            command_modules.append(module[:-3])
        except Exception as e:
            logger.error(f'Could not import module "{module[:-3]}": {e}')
except Exception as e:
    logger.error(f'Could not import cog modules: {e}')
    sys.exit(1)
finally:
    logger.info("Imported {} command modules: {}".format(
        len(command_modules),
        ', '.join(command_modules)
    )) if command_modules else logger.warn("Imported 0 command modules. Command availability limited")


class Finder(commands.Cog):
    """Main class for the Finder command

    Args:
        commands (string): Command
    """

    def __init__(self, client):
        "Init function for Discord client"

        self.client = client

    @Cog.listener()
    async def on_ready(self):
        "Function to determine what commands are to be executed if bot is connected to Discord"

        logger.info("Core cog up!")

    # END search_requester


def setup(bot):
    "Setup command for the bot"
    bot.add_cog(Finder(bot))
