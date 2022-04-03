import os
import re
from inspect import cleandoc

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

        self._api_repos_re = re.compile("(api.)|(/repos)")
        self._whitespace_re = re.compile(r"\s\s+")

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

        logger.info(f"{ctx.author.user.username} - intiated repolang command")
        logger.debug(f"args: {topics}")

        logger.info(f"{ctx.author.user.username} - initiated repolang")
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
            await ctx.send(content=cleandoc(f"""
                Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?

                Your query was:
                ```py
                Languages: \"{languages}\", Topics: \"{topics}\"
                ```
            """), ephemeral=True)
            return

        try:
            if languages == "" or topics == "" or resp["total_count"] == 0:
                logger.warning("Response returned zero results")
                await ctx.send(content=cleandoc(f"""
                    Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?

                    Your query was:
                    ```py
                    Languages: \"{languages}\", Topics: \"{topics}\"
                    ```
                """), ephemeral=True)
            else:
                repo_embed, embed_action_row = await process_embed.process_embed(resp, ctx)
                await ctx.send(
                    content=f"Found a new repo matching language(s) `{', '.join(languages)}`!",
                    embeds=repo_embed,
                    components=[embed_action_row],
                )
        except Exception as e:
            logger.warning(e, exc_info=1)
            await ctx.send(content=cleandoc(f"""
                Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?
                
                Your query was:
                ```py
                Languages: \"{languages}\", Topics: \"{topics}\"
                ```
            """), ephemeral=True)


def setup(client: interactions.Client):
    Repolang(client)
