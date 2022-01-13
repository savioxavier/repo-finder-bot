"""
This file provides a template for future commands.
This file will not be loaded as a cog or module
"""

import os
import interactions

# Highly recommended - we suggest providing proper debug logging
from src import logutil

"Uncomment if you need to interact with the interactions.Client instance"
# from src.bot import bot

"Uncomment if you want to check if a user has permissions"
# from src.permissions import Permissions, has_permission

# Change this if you'd like - this labels log messages for debug mode
logger = logutil.init_logger(os.path.basename(__file__))


# Rename this class to whatever you'd like.
#
# Your main class command that encompasses the command functions
# should end with a "CMD" (case insensitive).
# If not, your cog will not be loaded.
# This main class also gets the context passed when the command
# is triggered.
class CommandCMD():
    "Main class for bot"
    def __init__(self):
        # BEGIN cmd_config
        # What will your command respond to?
        self.NAME = "helloworld"

        # What does your command do?
        self.DESCRIPTION = "A simple hello world command"

        # Write your options code here
        # (not required. Can be empty)
        self.OPTIONS = []

        # What type of command is it?
        # (default: CHAT_INPUT)
        self.TYPE = interactions.ApplicationCommandType.CHAT_INPUT
        # END cmd_config
        logger.info("%s command module registered" %
                    __class__.__name__)

    # If you defined options above,
    # add them here in the keywords of the command()
    async def command(ctx):
        """
        Your command code goes here
        """
        await ctx.send("Hello!")

# You can have multiple classes for each command
# Just define another command class below
