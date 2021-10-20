"""
Meta commands script for the bot
"""

from discord.ext import commands
from discord.ext.commands import Cog
from discord_slash.utils.manage_components import create_actionrow, create_button
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext
import discord
import datetime as dt
import time
import os

DEV_GUILD = int(os.environ.get("DEV_GUILD"))
__GID__ = [846609621429780520]


class Meta(commands.Cog):
    """Main class for the Meta command

    Args:
        commands (string): Command
    """

    def __init__(self, client):
        "Init function for Discord client"

        self.client = client

        global bot_start_time
        bot_start_time = time.time()

    @Cog.listener()
    async def on_ready(self):
        "Function to determine what commands are to be if bot is connected to Discord"

        print("Meta up!")

    @cog_ext.cog_slash(name="info", description="Return details about the bot.", guild_ids=__GID__)
    async def _info(self, ctx):
        "Info command for the bot"

        info = discord.Embed(
            title="Bot Info",
            description="Information about the Repo Finder bot",
            color=0xd95025)

        info.set_author(
            name=f"{self.client.user.name}#{self.client.user.discriminator}", icon_url=self.client.user.avatar_url)

        uptime = dt.timedelta(
            seconds=int(round(time.time() - bot_start_time)))

        def strfdelta(tdelta, fmt):
            d = {"days": tdelta.days}
            d["hours"], rem = divmod(tdelta.seconds, 3600)
            d["minutes"], d["seconds"] = divmod(rem, 60)
            return fmt.format(**d)

        uptime = strfdelta(uptime, "{days} days, {hours} hours and {minutes} minutes")

        info.add_field(name="Uptime", value=uptime, inline=False)
        info.add_field(name="Default prefix", value="`rf.`", inline=False)
        info.add_field(name="Language used", value="Python", inline=False)
        info.add_field(name="Created by", value="Skyascii#1860", inline=False)
        info.add_field(name="Like this bot?",
                       value="Considering starring this project on [GitHub](https://github.com/savioxavier/repo-finder-bot)!", inline=False)
        info.set_thumbnail(url=self.client.user.avatar_url)
        info.set_footer(text="Repo Finder Bot")

        source_code_button = create_actionrow(create_button(
            style=ButtonStyle.URL, label="View Source Code", url="https://github.com/savioxavier/repo-finder-bot"))

        await ctx.send(embed=info, components=[source_code_button])


def setup(bot):
    "Setup command for the bot"

    bot.add_cog(Meta(bot))
