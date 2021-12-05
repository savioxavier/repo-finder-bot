import re
from os.path import dirname as dn

from discord.ext import commands
from discord.ext.commands import Cog

from utils import build_query, logutil, process_embed, requester
from utils.core import RequestError

Cog = commands.Cog


logger = logutil.initLogger("repolang.py")


class RepoLang(commands.Cog):

    _api_repos_re = re.compile("(api.)|(/repos)")
    _whitespace_re = re.compile(r"\s\s+")

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        logger.info("RepoLang command registered")

    # Find a repo by optional topic
    @commands.command(name="repolang")
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def command_find_repolang(self, ctx, languages: str = None, topics: str = None):
        logger.info(f"{ctx.message.author} - intiated repo command")
        logger.debug(f"args: {topics}")
        first_message = await ctx.send("Fetching a repo, just for you!")
        if languages is None or languages == "":
            logger.debug(
                f"{ctx.message.author} - initiated repolang with no required args")
            await first_message.edit(content="""You need to specify a language!
Example:```fix
rf.repolang \"python\"
```""")

        else:
            logger.info(f"{ctx.message.author} - initiated repolang")
            logger.debug(f"args: {languages} ; {topics}")

            # languages = languages.replace(" ", "").split(",")
            if "," in languages:  # if user separates by comma, split and strip spaces
                languages = [s.strip() for s in languages.split(",")]
            elif " " in languages:  # if user separates by space, strip duplicate spaces, and replace spaces with commas
                languages = self._whitespace_re.sub(" ", languages)
                languages = languages.replace(" ", ",").split(",")
            else:
                languages = [languages, ]
            payload = {
                'method': "repositories",
                'languages': languages,
            }

            if topics:
                if "," in topics:  # if user separates by comma, split and strip spaces
                    topics = [s.strip() for s in topics.split(",")]
                elif " " in topics:  # if user separates by space, strip duplicate spaces, and replace spaces with commas
                    topics = self._whitespace_re.sub(" ", topics)
                    topics = topics.replace(" ", ",").split(",")
                else:
                    topics = [topics]
                payload["topics"] = topics

            try:
                logger.info("Payload built. Sending to search_requester...")
                resp = await requester.requester(payload)
            except RequestError as e:
                # FIX: Logs random exceptions to the console
                logger.warning(e)
                await first_message.edit(content="Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?")
                return

            if languages == "" or topics == "" or resp["total_count"] == 0:
                await first_message.edit(content="Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?")
            else:
                repo_embed, embed_action_row = await process_embed.process_embed(resp, ctx)
                await first_message.edit(content="Found a new repo matching language(s) `{}`!".format(', '.join(languages)), embed=repo_embed, components=[embed_action_row])


def setup(bot):
    bot.add_cog(RepoLang(bot))
