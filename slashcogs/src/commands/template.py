"""
This file provides a template for future commands. This file will not be loaded as a cog or module
"""

import os
from discord.ext import commands

# You will need to import cog_ext from discord_slash in order to use slash commands
from discord_slash import cog_ext

# Import required Discord libraries
# Highly recommended - we suggest providing proper debug logging
from cogs.src import logutil

Cog = commands.Cog

# If your command requires the search_requester or process_embed functions...
"""
from cogs.src import (
    requester,
    build_query,
    process_embed
)
"""
# We highly suggest catching HTTP request exceptions with RequestError in core.py
"""
from core.core import logutil
"""

# Change this - this labels log messages for debug mode
logger = logutil.initLogger("template.py")

# Use the DEV_GUILD environment variable to instantly load slash commands in your testing guild. Global slash commands are usually cached for an hour due to Discord API restrictions.
DEV_GUILD = int(os.environ.get("DEV_GUILD"))


# Rename this class to whatever you'd like. Rename it again below at setup()
class Command(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):  # code to execute when cog has been loaded
        logger.info("Command slash cog registered")

    # Set this to your command name (eg: /command) and add a meaningful description. Don't forget to specify a value of [DEV_GUILD] to the guild_ids argument or your slash commands won't instantly load!
    @cog_ext.cog_slash(name="command", description="Some description.", guild_ids=[DEV_GUILD])
    # Pass all arguments as "args" and default to NoneType
    async def command(self, ctx, *, args: str = None):
        """
        Your command code goes here
        """

# Required for cog to register


def setup(bot):
    bot.add_cog(Command(bot))  # Don't forget to rename the class here!