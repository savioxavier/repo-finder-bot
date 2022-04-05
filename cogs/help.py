import os

import interactions

from config import DEV_GUILD
from utils import logutil

logger = logutil.init_logger(os.path.basename(__file__))

horizontal_rule = "━" * 10

BOT_HELP = f"""
• **`/help`**
> Displays this embed.
{horizontal_rule}
• **`/repo [topics]`**
> Find a repo with an optional topic(s). Topic defaults to `hacktoberfest`. Can also specify multiple topics:
```py
/repo topics:reactjs, webdev
```
You can specify multiple topics by separating them with a comma too, if spaces aren't your thing.
{horizontal_rule}
• **`repolang languages [topics]`**
> Find a repo with specified language and optional topic(s).
```py
/repolang languages:c, python topics:ai, webdev
```
- Language is **required**
- Like `/repo`, you can separate with either commas or spaces
{horizontal_rule}
• **`info`**
> Returns details about the bot.
"""


class Help(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        logger.info(f"{__class__.__name__} cog registered")

    @interactions.extension_command(
        name="help",
        description="Lists available commands for the Repo Finder Bot",
        scope=DEV_GUILD,
    )
    async def help_cmd(
        self,
        ctx: interactions.CommandContext,
    ):

        bot_user = interactions.User(**await self.client._http.get_self())

        bot_help = interactions.Embed(
            title="Available commands for Repo Finder Bot",
            description=BOT_HELP,
            color=0xD95025,
            author=interactions.EmbedAuthor(
                name=f"{bot_user.username}#{bot_user.discriminator}",
                icon_url=bot_user.avatar_url or None,
            ),
            thumbnail=interactions.EmbedImageStruct(url=bot_user.avatar_url),
            footer=interactions.EmbedFooter(text="Repo Finder Bot"),
        )

        await ctx.send(embeds=bot_help)


def setup(client: interactions.Client):
    Help(client)
