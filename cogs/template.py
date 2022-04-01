"""
This file provides a template for future commands.
This file will not be loaded as a cog or module
"""

# os module - required for obtaining the current file name for logging purposes
import os

# Main interactions-py module (discord-py-interactions)
import interactions

# Your DEV_GUILD is the ID of the guild/server in which development is done
from config import DEV_GUILD
# Highly recommended - we suggest providing proper debug logging
from utils import logutil

# Change this if you'd like - this labels log messages for debug mode
logger = logutil.init_logger(os.path.basename(__file__))


# Rename this class to whatever you'd like.
#
# This main class also gets the context passed when the command
# is triggered.
class CommandName():
    "Main class for bot"

    def __init__(self, client: interactions.Client):
        # Register the bot client with the class
        self.client: interactions.Client = client
        logger.info(f"{__class__.__name__} cog registered")

    # Use this decorator to register your command
    # The first parameter (name) is the name of the command
    # The second parameter (description) is the description of the command
    # The third parameter (scope) is the scope of the command (the guild in which development is done, ie, the DEV_GUILD)

    @interactions.extension_command(name="command", description="Short description of the command", scope=DEV_GUILD)
    async def help_cmd(
        self,
        ctx: interactions.CommandContext,
    ):
        """
        Your command code goes here
        """
        await ctx.send("Hello!")

# Finally, register this cog with the bot client
# using the setup function
# This will register the class as a cog
# and load it into the bot client


def setup(client: interactions.Client):
    CommandName(client)
