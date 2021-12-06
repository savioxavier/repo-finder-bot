"""
Meta commands script for the bot
"""

import datetime
import os
import time

import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (create_actionrow,
                                                   create_button)

from utils import logutil

logger = logutil.initLogger("meta.py")


DEV_GUILD = int(os.environ.get("DEV_GUILD"))


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

        logger.info("Info command registered - Meta cog up!")

    @commands.command(name="info")
    async def command_botinfo(self, ctx):
        "Info command for the bot"
        logger.debug(f"{ctx.message.author} - initiated info command")

        info = discord.Embed(
            title="Bot Info",
            value="Information about the Repo Finder bot",
            color=0xd95025,
            timestamp=ctx.message.created_at
        )

        info.set_author(
            name=f"{self.client.user.name}#{self.client.user.discriminator}",
            icon_url=self.client.user.avatar_url
        )

        uptime = datetime.timedelta(
            seconds=int(round(time.time() - bot_start_time)))

        def strfdelta(tdelta, fmt):
            d = {"days": tdelta.days}
            d["hours"], rem = divmod(tdelta.seconds, 3600)
            d["minutes"], d["seconds"] = divmod(rem, 60)
            return fmt.format(**d)

        uptime = strfdelta(
            uptime, "{days} days, {hours} hours and {minutes} minutes")

        info.add_field(name="Uptime", value=uptime, inline=False)
        info.add_field(name="Default prefix", value="`rf.`", inline=False)
        info.add_field(name="Language used", value="Python", inline=False)
        info.add_field(name="Created by", value="Skyascii#1860", inline=False)
        info.add_field(name="Like this bot?",
                       value="Considering starring this project on [GitHub](https://github.com/savioxavier/repo-finder-bot)!",
                       inline=False)
        info.set_thumbnail(url=self.client.user.avatar_url)
        info.set_footer(text="Repo Finder Bot")

        invite_bot_button = create_button(
            style=ButtonStyle.URL, label="Invite Bot", url="https://discord.com/api/oauth2/authorize?client_id=772682311346159616&permissions=2147871808&scope=bot%20applications.commands")

        source_code_button = create_button(
            style=ButtonStyle.URL, label="View Source Code", url="https://github.com/savioxavier/repo-finder-bot")

        embed_components = create_actionrow(
            invite_bot_button, source_code_button)

        await ctx.send(embed=info, components=[embed_components])


def setup(bot):
    "Setup command for the bot"

    bot.add_cog(Meta(bot))
