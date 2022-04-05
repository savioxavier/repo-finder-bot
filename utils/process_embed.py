import os
import random
import re
from inspect import cleandoc

import aiohttp
import interactions

from config import GH_TOKEN
from utils import logutil
from utils.core import RequestError

logger = logutil.init_logger(os.path.basename(__file__))


async def process_embed(resp, ctx):
    _api_repos_re = re.compile("(api.)|(/repos)")
    _whitespace_re = re.compile(r"\s\s+")

    logger.debug("Processing embed:\n{}\n...".format(list(resp)[0]))
    data2 = random.choice(resp["items"])
    repo_full_name = data2["full_name"]
    repo_description = data2["description"]
    repo_language = data2["language"]
    repo_owner_image = data2["owner"]["avatar_url"]
    repo_url = data2["html_url"]
    try:
        if "license" in data2 and "name" in data2["license"]:
            repo_license_name = data2["license"]["name"]
        else:
            repo_license_name = "None"
    except TypeError:
        repo_license_name = "None"
    issue_count = data2["open_issues_count"]
    stargazers_count = data2["stargazers_count"]
    forks_count = data2["forks_count"]
    repo_details = cleandoc(
        f"""
        Stars  ⭐ : {stargazers_count}
        Issues  ⚠️ : {issue_count}
        Forks  🍴 : {forks_count}
        License  🛡️ : {repo_license_name}
        """
    )
    issues_url = f"https://api.github.com/repos/{repo_full_name}/issues"
    issues_button_url = _api_repos_re.sub("", issues_url)

    # replace using regex
    try:
        logger.debug(f"Sending a query to repo {repo_full_name} for issues...")

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=60)
        ) as session:
            async with session.get(
                issues_url,
                headers={"Content-Type": "application/json", "Authorization": GH_TOKEN},
            ) as issue_response_get:
                issue_response = await issue_response_get.json()
    except Exception as e:  # noqa
        raise RequestError from e
    try:
        issue_title = issue_response[0]["title"]

        issue_link = _api_repos_re.sub("", issue_response[0]["url"])

        issue_desc = (
            f"**[#{str(issue_response[0]['number'])}]({issue_link})** "
            + f"opened by {issue_response[0]['user']['login']}"
        )
        if len(issue_response) > 0:
            issue_details = f"{issue_title}\n{issue_desc}"
        else:
            issue_details = "Looks like there are no issues for this repository!"
    except IndexError:
        issue_details = "Looks like there are no issues for this repository!"

    repo_topics = data2["topics"]

    list_of_all_topics = " ".join(map(str, repo_topics))

    logger.debug("Building embed...")

    _embed_fields = [
        interactions.EmbedField(name="Language", value=repo_language, inline=True),
        interactions.EmbedField(name="Stars", value=stargazers_count, inline=True),
        interactions.EmbedField(name="Details", value=repo_details, inline=False),
        interactions.EmbedField(
            name="Latest Issues", value=issue_details, inline=False
        ),
    ]

    if list_of_all_topics.replace(" ", "") != "":
        REPO_TOPICS_LIST = cleandoc(
            f"""
            ```fix
            {list_of_all_topics}
            ```
            """
        )

        _embed_fields.append(
            interactions.EmbedField(name="Topics", value=REPO_TOPICS_LIST, inline=False)
        )

    repo_button = interactions.Button(
        style=interactions.ButtonStyle.LINK, label="Go to Repository", url=repo_url
    )
    issue_button = interactions.Button(
        style=interactions.ButtonStyle.LINK, label="View Issues", url=issues_button_url
    )

    embed_action_row = interactions.ActionRow(components=[issue_button, repo_button])

    repo_embed = interactions.Embed(
        title=repo_full_name,
        url=repo_url,
        description=repo_description,
        color=0xD95025,
        thumbnail=interactions.EmbedImageStruct(url=repo_owner_image)._json,  # noqa
        fields=_embed_fields,
        footer=interactions.EmbedFooter(text="Repo Finder Bot"),
    )

    logger.debug("Embed built")

    return repo_embed, embed_action_row


# END process_embed
