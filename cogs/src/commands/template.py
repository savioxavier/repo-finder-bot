"""
This file provides a template for future commands. This file will not be loaded as a cog or module
"""

# Import required Discord libraries
from discord.ext import commands
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
from cogs.core import RequestError
"""

from cogs.src import logutil # Highly recommended - we suggest providing proper debug logging
logger = logutil.initLogger("template.py") # change this - this labels log messages for debug mode

class Command(commands.Cog): # Rename this class to whatever you'd like. Rename it again below at setup()
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self): # code to execute when cog has been loaded
        logger.info("Command cog registered")

    @commands.command(name="command") # set this to your command name. The bot will respond to this with the prefix next to it. ex: rf.command
    async def command(self, ctx, *, args: str = None): # Pass all arguments as "args" and default to NoneType
        """
        Your command code goes here
        """

# Required for cog to register
def setup(bot):
    bot.add_cog(Command(bot)) # Don't forget to rename the class here!