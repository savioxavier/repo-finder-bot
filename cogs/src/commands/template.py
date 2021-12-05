"""
This file provides a template for future commands. This file will not be loaded as a cog or module
"""

from discord.ext import commands

# Import required Discord libraries
# Highly recommended - we suggest providing proper debug logging
from utils import logutil

Cog = commands.Cog

# If your command requires the search_requester or process_embed functions...
"""
from utils import (
    requester,
    build_query,
    process_embed
)
"""
# We highly suggest catching HTTP request exceptions with RequestError in core.py
"""
from utils.core import RequestError
"""

# Change this - this labels log messages for debug mode
logger = logutil.initLogger("template.py")


# Rename this class to whatever you'd like. Rename it again below at setup()
class Command(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):  # code to execute when cog has been loaded
        logger.info("Command cog registered")

    # Set this to your command name. The bot will respond to this with the prefix next to it. eg: rf.command
    @commands.command(name="command")
    # Pass all arguments as "args" and default to NoneType
    async def command(self, ctx, *, args: str = None):
        """
        Your command code goes here
        """

# Required for cog to register


def setup(bot):
    bot.add_cog(Command(bot))  # Don't forget to rename the class here!
