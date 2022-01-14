"""
Meta commands script for the bot
"""

import datetime
import time

import interactions

from utils import logutil
from utils.core import get_bot_self
logger = logutil.init_logger("meta.py")

global bot_start_time
bot_start_time = time.time()


class MetaCmd:
    def __init__(self):
        self.NAME = "info"
        self.DESCRIPTION = "Show bot information"
        self.TYPE = None
        self.OPTIONS = None
        logger.info(f"{__class__.__name__} command class registered")

    async def command(ctx: interactions.CommandContext):
        """Info command for the bot"""
        bot_user = await get_bot_self()
        logger.debug(f"{ctx.author.user.username} - initiated info command")

        uptime = datetime.timedelta(
            seconds=int(round(time.time() - bot_start_time)))

        def strfdelta(tdelta, fmt):
            d = {"days": tdelta.days}
            d["hours"], rem = divmod(tdelta.seconds, 3600)
            d["minutes"], d["seconds"] = divmod(rem, 60)
            return fmt.format(**d)

        uptime = strfdelta(
            uptime, "{days} days, {hours} hours and {minutes} minutes")

        info = interactions.Embed(
            title="Bot Info",
            value="Information about the Repo Finder bot",
            color=0xd95025,
            author=interactions.EmbedAuthor(
                name=f"{bot_user.username}#{bot_user.discriminator}",
                icon_url=bot_user.avatar or None
            ),
            fields=[
                interactions.EmbedField(
                    name="Uptime",
                    value=uptime,
                    inline=False
                ),
                interactions.EmbedField(
                    name="Language used",
                    value="Python",
                    inline=False
                ),
                interactions.EmbedField(
                    name="Created by",
                    value="Skyascii#1860",
                    inline=True
                ),
                interactions.EmbedField(
                    name="Like this bot?",
                    value="Considering starring this project on " +
                          "[GitHub](https://github.com/savioxavier/repo-finder-bot)!",
                    inline=False
                )
            ],
            thumbnail=interactions.EmbedImageStruct(
                url=bot_user.avatar
            )._json,
            footer=interactions.EmbedFooter(
                text="Repo Finder Bot"
            )
        )

        invite_bot_button = interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="Invite Bot",
            url="https://discord.com/api/oauth2/authorize?client_id" +
                "=772682311346159616&permissions=2147871808&scope=bot%20applications.commands"
        )

        source_code_button = interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="View Source Code",
            url="https://github.com/savioxavier/repo-finder-bot"
        )

        embed_components = interactions.ActionRow(
            components=[invite_bot_button, source_code_button]
        )

        await ctx.send(embeds=info, components=embed_components)
