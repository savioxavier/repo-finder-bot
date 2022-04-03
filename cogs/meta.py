"""
Meta commands script for the bot
"""

import datetime
import os
import time

import interactions

from config import DEV_GUILD
from utils import logutil

logger = logutil.init_logger(os.path.basename(__file__))

global bot_start_time
bot_start_time = time.time()


class Meta(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        logger.info(f"{__class__.__name__} cog registered")

    @interactions.extension_command(name="info", description="View details about the bot", scope=DEV_GUILD)
    async def info_cmd(self, ctx: interactions.CommandContext):
        """Info command for the bot"""

        bot_user = interactions.User(** await self.client._http.get_self())

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
                icon_url=bot_user.avatar_url or None
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
                url=bot_user.avatar_url
            ),
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

        info.timestamp = datetime.datetime.utcnow()

        await ctx.send(embeds=info, components=embed_components)


def setup(client: interactions.Client):
    Meta(client)
