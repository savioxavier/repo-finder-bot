import os
from os.path import dirname as dn

from discord.ext import commands
from discord.ext.commands import Cog
from discord_slash import cog_ext

from cogs.core import RequestError, logutil
from cogs.src import build_query, logutil, process_embed, requester

logger = logutil.initLogger("repo.py")


DEV_GUILD = int(os.environ.get("DEV_GUILD"))


class Repo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        logger.info("Repo slash command registered")

    # Find a repo by optional topic
    @cog_ext.cog_slash(name="repo", description="Find a GitHub repoistory.", guild_ids=[DEV_GUILD])
    async def command_find_repo(self, ctx, *, topics: str = None):
        logger.info(f"{ctx.author} - intiated repo command")
        logger.debug(f"args: {topics}")
        first_message = await ctx.send("Fetching a repo, just for you!")
        if topics is None:
            topics = ["hacktoberfest", ]
        elif "," in topics:  # if user separates by comma, split and strip spaces
            topics = [s.strip() for s in topics.split(",")]
        elif " " in topics:  # if user separates by space, strip duplicate spaces, and replace spaces with commas
            # topics = " ".join(topics.split(" "))
            topics = self._whitespace_re.sub(" ", topics)
            topics = topics.replace(" ", ",").split(",")
        else:
            topics = [topics, ]
        payload = {
            'method': "repositories",
            'topics': topics
        }

        try:
            logger.info("Payload built. Sending to search_requester...")
            resp = await requester.requester(payload)
        except RequestError as e:
            # FIX: Logs random exceptions to the console
            logger.warning(e)
            await first_message.edit(content="Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?")
            return

        if resp["total_count"] == 0:
            logger.warning("Response returned zero results")
            await first_message.edit(content="Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?")
        else:
            # logger.debug("Processing results...\n{}\n...".format(list(resp)[0]))
            repo_embed, embed_action_row = await process_embed.process_embed(resp, ctx)
            await first_message.edit(content="Found a new repo matching topic(s) `{}`!".format(', '.join(topics)), embed=repo_embed, components=[embed_action_row])


def setup(bot):
    bot.add_cog(Repo(bot))