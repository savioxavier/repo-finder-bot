import os

import interactions

from utils import logutil, process_embed, requester
from utils.build_query import parse_args
from utils.core import RequestError

logger = logutil.init_logger("repo.py")
DEV_GUILD = int(os.environ.get("DEV_GUILD"))


class RepoCmd:
    def __init__(self):
        self.NAME = "repo"
        self.DESCRIPTION = "Search for repos by topic"
        self.OPTIONS = [
            interactions.Option(
                name="topics",
                description="Topic(s) to search. Separate by spaces or commas",
                type=interactions.OptionType.STRING,
                required=False
            )
        ]
        self.TYPE = None
        logger.info(f"{__class__.__name__} command class registered")

    # Find a repo by optional topic
    async def command(ctx: interactions.CommandContext, topics: str = "hacktoberfest"):
        await ctx.defer()
        logger.info(f"{ctx.author.user.username} - initiated repo command")
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
                repo_embed, embed_action_row = await process_embed.process_embed(resp, ctx)
                await ctx.send(content="Found a new repo matching topic(s) `{}`!".format(', '.join(parse_args(topics))),
                               embeds=[repo_embed],
                               components=[embed_action_row])
        except Exception:  # noqa
            logger.warn(exc_info=1)
            await ctx.send(content="Something went wrong trying to fetch data. " +
                                   "An incorrect query, perhaps? Maybe try the command again?")
