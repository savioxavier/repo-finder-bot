"""
Master script for the bot
"""

from discord.enums import Status
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv
import discord
import os

load_dotenv()

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
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes

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
    print(f"Logged in as {client.user.name}#{client.user.discriminator}!")


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
    except:
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
        await ctx.send(f"This command is on cooldown. Try again after `{round(error.retry_after)}` seconds.", delete_after=5)

client.load_extension("cogs.repo")
client.load_extension("cogs.meta")
client.run(TOKEN)
