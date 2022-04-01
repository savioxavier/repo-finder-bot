import os

import interactions

from config import DEV_GUILD
from utils import logutil, process_embed, requester
from utils.build_query import parse_args
from utils.core import RequestError

logger = logutil.init_logger(os.path.basename(__file__))


class Repo(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        logger.info(f"{__class__.__name__} cog registered")

    @interactions.extension_command(
        name="repo",
        description="Search for repos by topic",
        scope=DEV_GUILD,
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="topics",
                description="Topics to search for",
                required=False,
            )
        ],
    )
    async def repo_cmd(self, ctx: interactions.CommandContext, topics: str = "hacktoberfest"):

        await ctx.defer()
        logger.debug(f"args: {topics}")

        payload = {
            'method': "repositories",
            'topics': parse_args(topics)
        }

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
            if resp["total_count"] == 0:
                logger.warning("Response returned zero results")
                await ctx.send(content="Something went wrong trying to fetch data. " +
                                       "An incorrect query, perhaps? Maybe try the command again?")
            else:
                repo_embed, embed_action_row = await process_embed.process_embed(resp)
                await ctx.send(
                    content=f"Found a new repo matching topic(s) `{', '.join(parse_args(topics))}`!",
                    embeds=[repo_embed],
                    components=[embed_action_row],
                )

        except Exception:  # noqa
            logger.warn(exc_info=1)
            await ctx.send(content="Something went wrong trying to fetch data. " +
                                   "An incorrect query, perhaps? Maybe try the command again?")


def setup(client: interactions.Client):
    Repo(client)
