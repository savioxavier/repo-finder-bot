import os

import interactions

from config import DEV_GUILD
from utils import logutil

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


class Help(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        logger.info(f"{__class__.__name__} cog registered")

    @interactions.extension_command(name="help", description="Lists available commands for the Repo Finder Bot", scope=DEV_GUILD)
    async def help_cmd(
        self,
        ctx: interactions.CommandContext,
    ):
        bot_help = interactions.Embed(
            title="Available commands for Repo Finder Bot",
            description=BOT_HELP,
            color=0xd95025,
        )
        await ctx.send(embeds=bot_help)


def setup(client: interactions.Client):
    Help(client)
