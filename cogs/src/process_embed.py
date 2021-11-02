from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (
    create_actionrow,
    create_button
)

from cogs.core import RequestError, GH_TOKEN

import discord
import random
import aiohttp
import re

from . import logutil
logger = logutil.initLogger("processs_embed.py")

# Process the search_requester response into an embed we can send
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
    if "license" in data2 and "name" in data2["license"]:
        repo_license_name = data2["license"]["name"]
    else:
        repo_license_name = "None"
    issue_count = data2["open_issues_count"]
    stargazers_count = data2["stargazers_count"]
    forks_count = data2["forks_count"]
    REPO_DETAILS = f"""
Stars  ⭐ : {stargazers_count}
Issues  ⚠️ : {issue_count}
Forks  🍴 : {forks_count}
License  🛡️ : {repo_license_name}
    """
    issues_url = f"https://api.github.com/repos/{repo_full_name}/issues"
    issues_button_url = _api_repos_re.sub("", issues_url)
    # replace using regex
    try:
        logger.debug(f"Sending a query to repo {repo_full_name} for issues...")
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.get(issues_url, headers={"Content-Type": "application/json", "Authorization": GH_TOKEN}) as issue_response_get:
                issue_response = await issue_response_get.json()
    except:
        raise RequestError
    try:
        issue_title = issue_response[0]['title']

        issue_link = _api_repos_re.sub(
            "", issue_response[0]['url']
        )
        # replace using regex

        issue_desc = f"**[#{str(issue_response[0]['number'])}]({issue_link})** opened by {issue_response[0]['user']['login']}"
        if len(issue_response) > 0:
            ISSUE_DETAILS = f"{issue_title}\n{issue_desc}"
        else:
            ISSUE_DETAILS = "Looks like there are no issues for this repository!"
    except IndexError:
        ISSUE_DETAILS = "Looks like there are no issues for this repository!"
    repo_topics = data2["topics"]
    list_of_all_topics = " ".join(map(str, repo_topics))
    REPO_TOPICS_LIST = f"""```fix
{list_of_all_topics}
```
    """

    logger.debug("Building embed...")
    repo_button = create_button(
        style=ButtonStyle.URL, label="Go to Repository",
        url=repo_url
    )
    issue_button = create_button(
        style=ButtonStyle.URL, label="View Issues",
        url=issues_button_url
    )
    embed_action_row = create_actionrow(
        issue_button, repo_button
    )
    repo_embed = discord.Embed(
        title=repo_full_name, url=repo_url,
        description=repo_description, color=0xd95025,
        timestamp=ctx.message.created_at
    )
    repo_embed.set_thumbnail(url=repo_owner_image)
    repo_embed.add_field(
        name="Language", value=repo_language, inline=True
    )
    repo_embed.add_field(
        name="Stars", value=stargazers_count, inline=True
    )
    repo_embed.add_field(
        name="Details", value=REPO_DETAILS, inline=False
    )
    repo_embed.add_field(
        name="Latest Issues", value=ISSUE_DETAILS, inline=False
    )
    repo_embed.set_footer(text="Repo Finder Bot")

    if len(list_of_all_topics.replace(" ", "")) > 0:
        repo_embed.add_field(
            name="Topics", value=REPO_TOPICS_LIST, inline=False)
    logger.debug("Embed built")

    return repo_embed, embed_action_row

# END process_embed