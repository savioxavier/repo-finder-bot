import os

import interactions

from utils import logutil
from utils.core import get_bot_self

logger = logutil.init_logger(os.path.basename(__file__))

BOT_HELP = """
• `/help`
> Displays this embed.

• `/repo [topic] [topic]`
> Find a repo with an optional topic(s). Topic defaults to `hacktoberfest`. Can also specify multiple topics:

```py
/repo reactjs webdev
```
You can specify multiple topics by separating them with a comma too, if spaces aren't your thing.

• `repolang languages: [topic:]`
> Find a repo with specified language.

```py
rf.repolang languages:c, python topics:ai, webdev
```
- Language is **required**
- Like `/repo`, you can separate with either commas or spaces

• `info`
> Returns details about the bot.
"""


class HelpCmd:
    def __init__(self):
        self.NAME = "help"
        self.TYPE = None
        self.OPTIONS = None
        self.DESCRIPTION = "Display help information"
        logger.info(f"{__class__.__name__} command class registered")

    async def command(ctx: interactions.CommandContext):
        """Main help command for the bot"""
        logger.debug(f"{ctx.author.user.username} - initiated help command")
        _bot_user = await get_bot_self()

        bot_help = interactions.Embed(
            title="Available commands for Repo Finder Bot",
            description=BOT_HELP,
            color=0xd95025,
            thumbnail=interactions.EmbedImageStruct(
                url=_bot_user.avatar or None
            )._json,
            footer=interactions.EmbedFooter(
                text="Repo Finder Bot"
            )
        )
        await ctx.send(embeds=bot_help)