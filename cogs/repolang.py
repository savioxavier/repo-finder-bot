import os

import interactions

from config import DEV_GUILD
from utils import logutil, process_embed, requester
from utils.build_query import parse_args
from utils.core import RequestError

logger = logutil.init_logger(os.path.basename(__file__))


class Repolang(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        logger.info(f"{__class__.__name__} cog registered")

    @interactions.extension_command(
        name="repolang",
        description="Search repos by language and optional topic",
        scope=DEV_GUILD,
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="languages",
                description="Language(s) to search. Separate by spaces or commas",
                required=True,
            ),
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="topics",
                description="Topic(s) to search for. Separate by spaces or commas",
                required=False,
            )
        ],
    )
    async def repolang_cmd(self, ctx: interactions.CommandContext, languages: str = None, topics: str = None):
        await ctx.defer()

        logger.debug(
            "Got args from user:\ntopics: '%s'\nlanguages: '%s'" % (topics, languages))

        if languages is None or not languages:
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
                if not topics or resp["total_count"] == 0:
                    await ctx.send(content="Something went wrong trying to fetch data. " +
                                           "An incorrect query, perhaps? Maybe try the command again?")
                else:
                    repo_embed, embed_action_row = await process_embed.process_embed(resp, ctx)
                    _content = f"Found a new repo matching language(s) `{', '.join(parse_args(languages))}`"

                    _content += f" and topics {', '. join(parse_args(topics))}" if topics else ""
                    await ctx.send(
                        content=f'{_content}!',
                        embeds=[repo_embed],
                        components=[embed_action_row],
                    )

            except Exception as e:  # noqa
                logger.warning(e)
                await ctx.send(content="Something went wrong trying to fetch data. " +
                                       "An incorrect query, perhaps? Maybe try the command again?")


def setup(client: interactions.Client):
    Repolang(client)
