"""
Master script for the bot
"""

import os

import discord
from discord.enums import Status
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

from utils import logutil
from utils.common import DEBUG, DEBUG_DISCORD

load_dotenv()

# Configure logging for this (main.py) handler
logger = logutil.initLogger("main.py")

# Configure logging for discord.py
if DEBUG:
    logging = logutil.getLogger("discord")

logger.warning(f"Debug mode is {DEBUG} || Discord debug mode is {DEBUG_DISCORD}")

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
        logger.debug(
            f"Custom prefix is '{custom_prefixes.get(guild.id, default_prefixes)}'")
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        logger.debug(f"Using default prefix '{default_prefixes}'")
        return default_prefixes

logger.debug("Initial presence set")
activity = discord.Game(name="rf.help • /help")
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
    logger.info(
        f"Logged in as {client.user.name}#{client.user.discriminator}!")


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
• **`help`**, Slash equivalent: **`/help`**
> Displays this embed.

• **`repo [topic] [topic]`**, Slash equivalent: **`/repo`**
> Find a repo with an optional topic(s). Topic defaults to `hacktoberfest`. Can also specify multiple topics:

```py
rf.repo reactjs webdev
```
You can specify multiple topics by separating them with a comma too, if spaces aren't your thing.

• **`repolang (languages) [topic]`**, Slash equivalent: **`/repolang`**
> Find a repo with specified language.

```py
rf.repolang \"c, python\" \"ai, webdev\"
```
- Double quotes are **required** if searching for multiple languages or topics
- Language is **required**
- Like `rf.repo`, you can separate with either commas or spaces

• **`setprefix [prefix]`**
> Change prefix of the bot.

• **`info`**, Slash equivalent: `/info`
> Returns details about the bot.

_Slash commands are available! They are specified right next to the regular commands in this embed._
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


@slash.slash(name="help", description="List commands",  guild_ids=[DEV_GUILD])
async def command_help(ctx):
    "Main help command for the bot"
    logger.debug(f"{ctx.author} - initiated help slash command")

    bot_help = discord.Embed(
        title="Available commands for Repo Finder Bot",
        description=BOT_HELP,
        color=0xd95025,
        timestamp=ctx.created_at)

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
        await ctx.send(f"A discord.py command error occured:```{error}```Try your command again")

client.load_extension("utils.core")

command_modules = [
    module[:-3]
    for module in os.listdir(f"{os.path.dirname(__file__)}/cogs")
    if module not in ("__init__.py", "template.py") and module[-3:] == ".py"
]

if command_modules:
    logger.info('Importing {} cogs: {}'.format(
        len(command_modules),
        ', '.join(command_modules)
    ))
else:
    logger.warning("Could not import any cogs!")

# dynamically load all cogs found in cogs/src/commmands as cog extensions
for module in command_modules:
    try:
        client.load_extension("cogs." + module)
    except Exception as e:
        logger.error(f"Could not import cog {module}: \n{e}")

logger.info("Cog init complete. Cogs should be coming up soon")
logger.debug("\n\nCogs incoming:\n{}\n\n".format(
    ',\n'.join(command_modules)
))
client.run(TOKEN)
