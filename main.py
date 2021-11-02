"""
Master script for the bot
"""

import os
import logging

import discord
from discord.enums import Status
from discord.ext import commands
from discord_slash import SlashCommand
from cogs.src import logutil

from cogs.src.logutil import CustomFormatter
from cogs.src.common import USE_COLOR, DEBUG
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="[%(asctime)s][%(levelname)7s][%(funcName)20s][%(lineno)4s] %(message)s",
    # if DEBUG
    # else "[%(asctime)s][%(levelname)7s] %(message)s", # this stupid code doesn't work anymore. Put it in logutil.py
    datefmt="%I:%M.%S%p",
)

if USE_COLOR:
    root = logging.getLogger()
    hdlr = root.handlers[0]
    hdlr.setFormatter(CustomFormatter())

# Configure logging for this (main.py) handler
logger = logutil.initLogger("main.py")

logger.warning(f"Debug mode is {DEBUG}")

DEV_GUILD = int(os.environ.get("DEV_GUILD"))
TOKEN = os.environ.get("TOKEN")


__GUILD_ID__ = [DEV_GUILD]

custom_prefixes = {}
default_prefixes = ["rf."]


intents = discord.Intents.default()
intents.members = True


async def determine_prefix(bot, message):
    "Determine prefix for the bot"

    guild = message.guild

    if guild:
        logger.debug(f"Custom prefix is '{custom_prefixes.get(guild.id, default_prefixes)}'")
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        logger.debug(f"Using default prefix '{default_prefixes}'")
        return default_prefixes

logger.debug("Initial presence set")
activity = discord.Game(name="rf.help")
client = commands.Bot(command_prefix=determine_prefix,
                      case_insensitive=True,
                      activity=activity,
                      intents=intents,
                      help_command=None,
                      status=Status.idle
                      )
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)


@client.event
async def on_ready():
    "Function to determine what commands are to be if bot is connected to Discord"
    logger.info(f"Logged in as {client.user.name}#{client.user.discriminator}!")


@client.command()
@commands.guild_only()
async def setprefix(ctx, *, prefixes=""):
    """Function to change bot prefix from the default

    Args:
        prefixes (str, optional): Prefix to be used. Defaults to "".
    """
    try:
        custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefixes

        await ctx.send("Prefixes set for this guild!")
        logger.debug(f"Set prefix: {prefixes} for guild.id: {ctx.guild.id}")
    except:
        logger.warning(f"Prefix set failed for guild.id: {ctx.guild.id}")
        await ctx.send("Something went wrong trying to set prefixes for this guild.")


BOT_HELP = """
**`help`** - Displays this embed.

**`repo [topic] [topic]`** - Find a repo with an optional topic(s). Topic defaults to `hacktoberfest`. Can also specify multiple topics:
```py
rf.repo python hacktoberfest
```
or:
```py
rf.repo python, hacktoberfest
```

**`repolang (languages) [topic]`** - Find a repo with specified language.
Example:
```py
rf.repolang \"c, py\" \"hacktoberfest, c\"
```
- Double quotes are **required** if searching for multiple languages or topics
- Language is **required**
- Like `rf.repo`, you can separate with either commas or spaces

**`setprefix [prefix]`** - Change prefix of the bot.

**`info`** - Returns details about the bot.

_Slash commands coming soon!_
"""

# Regular help command


@client.command(name="help", description="List commands")
async def command_help(ctx):
    "Main help command for the bot"
    logger.debug(f"{ctx.message.author} - initiated help command")

    bot_help = discord.Embed(
        title="Available commands for Repo Finder Bot",
        description=BOT_HELP,
        color=0xd95025,
        timestamp=ctx.message.created_at)

    bot_help.set_thumbnail(url=client.user.avatar_url)
    bot_help.set_footer(text="Repo Finder Bot")

    await ctx.send(embed=bot_help)


@client.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        logger.debug(f"{ctx.message.author} - initiated a command on cooldown")
        await ctx.send(f"This command is on cooldown. Try again after `{round(error.retry_after)}` seconds.", delete_after=5)
    else:
        logger.warning(f"A discord.py command error occured:\n{error}")

client.load_extension("cogs.repo")
client.load_extension("cogs.meta")

logger.info("Cog loading complete")
client.run(TOKEN)
