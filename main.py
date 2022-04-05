"""
Master script for the bot
"""

import os

import interactions
from dotenv import load_dotenv

from config import DEBUG, TOKEN
from utils import logutil

load_dotenv()

# Configure logging for this main.py handler
logger = logutil.init_logger("main.py")

logger.debug(
    "Debug mode is %s; This is not a warning, just an indicator. You may safely ignore",
    DEBUG,
)


client = interactions.Client(
    token=TOKEN,
    disable_sync=False,
    presence=interactions.ClientPresence(
        status=interactions.StatusType.ONLINE,
        activities=[
            interactions.PresenceActivity(
                type=interactions.PresenceActivityType.GAME, name="/help"
            )
        ],
    ),
)


@client.event
async def on_ready():
    """Called when bot is ready to receive interactions"""

    bot_user = bot_user = interactions.User(**await client._http.get_self())

    logger.info(f"Logged in as {bot_user.username}#{bot_user.discriminator}")


# Dynamic cog loader (dynamic command registration)
# Fill this array with Python files in /cogs.
# This omits __init__.py, template.py, and excludes files without a .py file extension
cogs = [
    module[:-3]
    for module in os.listdir(f"{os.path.dirname(__file__)}/cogs")
    if module not in ("__init__.py", "template.py") and module[-3:] == ".py"
]

logger.info("Importing %s cogs: %s", len(cogs), ", ".join(cogs))
for cog in cogs:
    try:
        client.load(f"cogs.{cog}")
    except Exception as e:
        logger.error(f"Could not load a cog: {cog}", exc_info=DEBUG)
        logger.error(e)

client.start()
