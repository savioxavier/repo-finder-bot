from discord.ext import commands
from discord.ext.commands import Cog
from os.path import dirname as dn

import logging
from cogs.core import RequestError

from cogs.src import (
    requester,
    build_query,
    process_embed
)

class Repo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        logging.info("Repo command registered")

    # Find a repo by optional topic
    @commands.command(name="repo")
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def command_find_repo(self, ctx, *, topics: str = None):
        logging.info(f"{ctx.message.author} - intiated repo command")
        logging.debug(f"args: {topics}")
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
            logging.info("Payload built. Sending to search_requester...")
            resp = await requester.requester(payload)
        except RequestError as e:
            # FIX: Logs random exceptions to the console
            logging.warning(e)
            await first_message.edit(content="Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?")
            return

        if resp["total_count"] == 0:
            logging.warning("Response returned zero results")
            await first_message.edit(content="Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?")
        else:
            # logging.debug("Processing results...\n{}\n...".format(list(resp)[0]))
            repo_embed, embed_action_row = await process_embed.process_embed(resp, ctx)
            await first_message.edit(content="Found a new repo matching topic(s) `{}`!".format(', '.join(topics)), embed=repo_embed, components=[embed_action_row])

def setup(bot):
    bot.add_cog(Repo(bot))