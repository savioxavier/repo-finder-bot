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
