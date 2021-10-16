"""
Repo Finder command script for the bot
"""

from discord.ext import commands
from discord.ext.commands import Cog
from discord_slash.utils.manage_components import create_actionrow, create_button
from discord_slash.model import ButtonStyle
import discord
import requests
import random
import os
import re

DEV_GUILD = int(os.environ.get("DEV_GUILD"))
GH_TOKEN = os.environ.get("GH_TOKEN")

__GUILD_IDS__ = [DEV_GUILD]


class Finder(commands.Cog):
    """Main class for the Finder command

    Args:
        commands (string): Command
    """

    def __init__(self, client):
        "Init function for Discord client"

        self.client = client

    @Cog.listener()
    async def on_ready(self):
        "Function to determine what commands are to be if bot is connected to Discord"

        print("Finder up!")

    @commands.command(name="repo")
    async def command_find_repo(self, ctx, *, arg: str = "hacktoberfest"):

        target_topic = arg.replace(" ", "-")

        first_message = await ctx.send("Fetching a repo, just for you!")

        url = f"https://api.github.com/search/repositories?q=topic:{target_topic}&per_page=75"

        response = requests.get(url, headers={"Content-Type": "application/json",
                                              "Authorization": GH_TOKEN})

        resp = response.json()

        if resp["total_count"] == 0:
            # FIX: Logs random exceptions to the console
            await first_message.edit(content="Something went wrong trying to fetch data. An incorrect topic, perhaps? Maybe try the command again?")

        data2 = random.choice(resp["items"])

        repo_full_name = data2["full_name"]
        repo_description = data2["description"]
        repo_language = data2["language"]
        repo_owner_image = data2["owner"]["avatar_url"]
        repo_url = data2["html_url"]
        repo_license_name = data2["license"]["name"]
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

        issues_button_url = re.sub(
            "(api.)|(/repos)", "", issues_url)  # replace using regex

        issue_response_get = requests.get(
            issues_url, headers={"Content-Type": "application/json",
                                 "Authorization": GH_TOKEN})

        issue_response = issue_response_get.json()

        issue_title = issue_response[0]['title']
        issue_link = issue_response[0]['url']
        issue_link = re.sub("(api.)|(/repos)", "",
                            issue_link)  # replace using regex
        issue_desc = f"**[#{str(issue_response[0]['number'])}]({issue_link})** opened by {issue_response[0]['user']['login']}"

        ISSUE_DETAILS = f"{issue_title}\n{issue_desc}" if issue_response != [
        ] else "Looks like there are no issues for this repository!"

        repo_topics = data2["topics"]

        list_of_all_topics = " ".join(map(str, repo_topics))

        REPO_TOPICS_LIST = f"""```fix
{list_of_all_topics}
```
        """

        repo_button = create_button(
            style=ButtonStyle.URL, label="Go to Repository", url=repo_url)

        issue_button = create_button(
            style=ButtonStyle.URL, label="View Issues", url=issues_button_url)

        embed_action_row = create_actionrow(issue_button, repo_button)

        repo_embed = discord.Embed(title=repo_full_name, url=repo_url,
                                   description=repo_description, color=0xd95025, timestamp=ctx.message.created_at)

        repo_embed.set_thumbnail(url=repo_owner_image)
        repo_embed.add_field(
            name="Language", value=repo_language, inline=True)
        repo_embed.add_field(
            name="Stars", value=stargazers_count, inline=True)
        repo_embed.add_field(
            name="Details", value=REPO_DETAILS, inline=False)
        repo_embed.add_field(
            name="Latest Issues", value=ISSUE_DETAILS, inline=False)
        repo_embed.set_footer(text="Repo Finder Bot")

        repo_embed.add_field(
            name="Topics", value=REPO_TOPICS_LIST, inline=False)

        await first_message.edit(content=f"Found a new repo matching topic `{target_topic}`!", embed=repo_embed, components=[embed_action_row])


def setup(bot):
    "Setup command for the bot"

    bot.add_cog(Finder(bot))
