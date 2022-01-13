import re
import os

import interactions

from utils import logutil, process_embed, requester
from utils.build_query import parse_args
from utils.core import RequestError

logger = logutil.init_logger("repolang.py")
DEV_GUILD = int(os.environ.get("DEV_GUILD"))


class RepoLangCmd:
    def __init__(self):
        self.NAME = "repolang"
        self.DESCRIPTION = "Search repos by language and optional topic"
        self.OPTIONS = [
            interactions.Option(
                name="languages",
                description="Language(s) to search. Separate by spaces or commas",
                type=interactions.OptionType.STRING,
                required=True
            ),
            interactions.Option(
                name="topics",
                description="Topic(s) to search. Separate by spaces or commas",
                type=interactions.OptionType.STRING,
                required=False
            )
        ]
        self.TYPE = interactions.ApplicationCommandType.CHAT_INPUT
        logger.info(f"{__class__.__name__} command class registered")

    # Find a repo by optional topic
    async def command(ctx: interactions.CommandContext, languages: str = None, topics: str = None):
        await ctx.defer()
        logger.debug("Got args from user:\ntopics: '%s'\nlanguages: '%s'" % (topics, languages))
        if languages is None or languages == "":
            logger.debug(
                f"{ctx.author.user.username} - initiated repolang with no required args")
            await ctx.send(content="""You need to specify a language!
Example:```fix
/repolang \"python\"
```""")

        else:
            logger.info(f"{ctx.author.user.username} - initiated repolang")
            logger.debug(f"args: {languages} ; {topics}")

            payload = {
                'method': "repositories",
                'languages': parse_args(languages),
            }

            if topics:
                payload["topics"] = parse_args(topics)

            try:
                logger.info("Payload built. Sending to search_requester...")
                resp = await requester.requester(payload)
            except RequestError as e:
                # FIX: Logs random exceptions to the console
                logger.warning(e)
                await ctx.send(content="Something went wrong trying to fetch data. " +
                                       "An incorrect query, perhaps? Maybe try the command again?")
                return

            try:
                if languages == "" or topics == "" or resp["total_count"] == 0:
                    await ctx.send(content="Something went wrong trying to fetch data. " +
                                           "An incorrect query, perhaps? Maybe try the command again?")
                else:
                    repo_embed, embed_action_row = await process_embed.process_embed(resp, ctx)
                    _content = "Found a new repo matching language(s) `{}`".format(
                            ', '.join(parse_args(languages))
                        )
                    _content += " and topics {}".format(', '. join(parse_args(topics))) if topics else ""
                    await ctx.send(
                        content=_content + "!",
                        embeds=[repo_embed],
                        components=[embed_action_row]
                    )
            except Exception:  # noqa
                logger.warn(exc_info=1)
                await ctx.send(content="Something went wrong trying to fetch data. " +
                                       "An incorrect query, perhaps? Maybe try the command again?")
