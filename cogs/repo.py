"""
Repo Finder command script for the bot
"""

import os
import random
import re

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (create_actionrow,
                                                   create_button)
from requests.utils import requote_uri

DEV_GUILD = int(os.environ.get("DEV_GUILD"))
GH_TOKEN = str(os.environ.get("GH_TOKEN"))

__GUILD_IDS__ = [DEV_GUILD]


class RequestError(Exception):
    pass


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

    """ This will handle all search requests from now on. Provides modularity for future search commands """
    async def search_requester(self, payload):
        """ Our payload structure example:
        payload = {
            # For now, search for open issues, repo topics, and repo languages
            'method': 'repositories',                        # https://docs.github.com/en/rest/reference/search
            'topics': ['hacktoberfest', 'hacktoberfest2021'] # Will be defaulted to 'hacktoberfest'

            'languages': ['python', 'javascript'],
            'issue': {
                'isOpen': False,                             # https://docs.github.com/en/rest/reference/search#search-issues-and-pull-requests
                'type': 'issue'                              # https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests
                                                             # type can be "issue" or "pr"
            },
            'searchQuery': 'add command handler'
        }
        """
        # Now how do we conditionally add in these args to a search query? Warning: incoming mess
        # improve later please!
        """ Example query based on above payload example (excluding issue example):
            https://api.github.com/search/repositories?q=topic:hacktoberfest+topic:hacktoberfest2021+language:python+language:javascript+'add command handler'
                                         {method}              {topics}                              {languages}                         {searchQuery}
        """
        unbuiltQuery = ""

        # Build the query. If key contains multiple values, parse and append as required
        for key in payload:
            if key in ["topics", "languages"]:
                if len(payload[key]) > 1:
                    for i in payload[key]:
                        try:
                            # Prevent malformed queries by appending a "+" at the end if there is none
                            unbuiltQuery += "+" if unbuiltQuery[-1] != "+" else ""
                        except IndexError:  # if the unbuiltQuery is empty, do nothing
                            pass
                        if key == "languages":
                            unbuiltQuery += "language:{}+".format(i)
                        else:
                            unbuiltQuery += "topic:{}+".format(i)
                else:
                    try:
                        # Prevent malformed queries by appending a "+" at the end if there is none
                        unbuiltQuery += "+" if unbuiltQuery[-1] != "+" else ""
                    except:  # if the unbuiltQuery is empty, do nothing
                        pass
                    if key == "languages":
                        unbuiltQuery += "language:{}+".format(
                            payload["languages"][0])
                    else:
                        unbuiltQuery += "topic:{}+".format(
                            payload["topics"][0])
            elif key == "issue":
                if payload[key]:
                    unbuiltQuery += "is:issue+" if payload["issue"]["type"] == "issue" else "is:pr+"
                    # "is:closed+"?
                    unbuiltQuery += "is:open+" if payload["issue"]["isOpen"] is True else ""
            elif key == "searchQuery":
                if payload[key]:
                    unbuiltQuery += "\"{}\"".format(
                        payload["searchQuery"]) if payload["searchQuery"] else ""

        url = "https://api.github.com/search/{}?q={}&per_page=75".format(
            payload["method"], requote_uri(unbuiltQuery))  # encode and build the query

        response = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={"Content-Type": "application/json", "Authorization": GH_TOKEN}) as response:
                    return await response.json()
        except:
            raise RequestError
    # END search_requester

    # Process the search_requester response into an embed we can send
    async def process_embed(self, response, ctx):
        resp = response

        data2 = random.choice(resp["items"])
        repo_full_name = data2["full_name"]
        repo_description = data2["description"]
        repo_language = data2["language"]
        repo_owner_image = data2["owner"]["avatar_url"]
        repo_url = data2["html_url"]
        try:
            repo_license_name = data2["license"]["name"]
        except TypeError:  # encountered a NoneType once
            repo_license_name = "None"
            pass
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
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(issues_url, headers={"Content-Type": "application/json", "Authorization": GH_TOKEN}) as issue_response_get:
                    issue_response = await issue_response_get.json()
        except:
            issue_response = None
            raise RequestError
        try:
            issue_title = issue_response[0]['title']
            issue_link = issue_response[0]['url']
            issue_link = re.sub("(api.)|(/repos)", "",
                                issue_link)  # replace using regex
            issue_desc = f"**[#{str(issue_response[0]['number'])}]({issue_link})** opened by {issue_response[0]['user']['login']}"
            ISSUE_DETAILS = f"{issue_title}\n{issue_desc}" if issue_response != [
            ] else "Looks like there are no issues for this repository!"
        except IndexError:
            ISSUE_DETAILS = "Looks like there are no issues for this repository!"
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
        self.embed_action_row = create_actionrow(issue_button, repo_button)
        self.repo_embed = discord.Embed(title=repo_full_name, url=repo_url,
                                        description=repo_description, color=0xd95025, timestamp=ctx.message.created_at)
        self.repo_embed.set_thumbnail(url=repo_owner_image)
        self.repo_embed.add_field(
            name="Language", value=repo_language, inline=True)
        self.repo_embed.add_field(
            name="Stars", value=stargazers_count, inline=True)
        self.repo_embed.add_field(
            name="Details", value=REPO_DETAILS, inline=False)
        self.repo_embed.add_field(
            name="Latest Issues", value=ISSUE_DETAILS, inline=False)
        self.repo_embed.set_footer(text="Repo Finder Bot")
        # this is dumb code, I know. Just determines if there are any topics. If not, skip adding to embed
        if " ".join(repo_topics).replace(" ", "") != "":
            self.repo_embed.add_field(
                name="Topics", value=REPO_TOPICS_LIST, inline=False)

        return
    # END process_embed

    # Find a repo by optional topic
    @commands.command(name="repo")
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def command_find_repo(self, ctx, *, topics: str = None):
        first_message = await ctx.send("Fetching a repo, just for you!")
        if topics is None:
            topics = ["hacktoberfest", ]
        elif "," in topics:  # if user separates by comma, split and strip spaces
            topics = topics.split(",")
            topics = [s.strip() for s in topics]
        elif " " in topics:  # if user separates by space, strip duplicate spaces, and replace spaces with commas
            # topics = " ".join(topics.split(" "))
            topics = re.sub("\s\s+", " ", topics)
            topics = topics.replace(" ", ",").split(",")
        else:
            topics = [topics, ]
        payload = {
            'method': "repositories",
            'topics': topics
        }

        try:
            resp = await self.search_requester(payload)
        except RequestError as e:
            # FIX: Logs random exceptions to the console
            print(e)
            await first_message.edit(content="Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?")

        if resp["total_count"] == 0:
            await first_message.edit(content="Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?")
        else:
            await self.process_embed(resp, ctx)
            await first_message.edit(content="Found a new repo matching topic(s) `{}`!".format(', '.join(topics)), embed=self.repo_embed, components=[self.embed_action_row])

    # Find a repo by language and optional topic
    # ex. rf.repo "c,py,php" "hacktoberfest"
    @commands.command(name="repolang")
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def command_find_repolang(self, ctx, languages: str = None, topics: str = None):
        first_message = await ctx.send("Fetching a repo, just for you!")
        if languages is None:
            await first_message.edit(content="""You need to specify a language!
Example:```
rf.repolang \"python\"
```""")
        else:
            # languages = languages.replace(" ", "").split(",")
            if "," in languages:  # if user separates by comma, split and strip spaces
                languages = languages.split(",")
                languages = [s.strip() for s in languages]
            elif " " in languages:  # if user separates by space, strip duplicate spaces, and replace spaces with commas
                languages = re.sub("\s\s+", " ", languages)
                languages = languages.replace(" ", ",").split(",")
            else:
                languages = [languages, ]
            payload = {
                'method': "repositories",
                'languages': languages,
            }

            if topics:
                if "," in topics:  # if user separates by comma, split and strip spaces
                    topics = topics.split(",")
                    topics = [s.strip() for s in topics]
                elif " " in topics:  # if user separates by space, strip duplicate spaces, and replace spaces with commas
                    topics = re.sub("\s\s+", " ", topics)
                    topics = topics.replace(" ", ",").split(",")
                else:
                    topics = [topics, ]
                payload["topics"] = topics

            try:
                resp = await self.search_requester(payload)
            except RequestError as e:
                # FIX: Logs random exceptions to the console
                print(e)
                await first_message.edit(content="Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?")

            if resp["total_count"] == 0:
                await first_message.edit(content="Something went wrong trying to fetch data. An incorrect query, perhaps? Maybe try the command again?")
            else:
                await self.process_embed(resp, ctx)
                await first_message.edit(content="Found a new repo matching language(s) `{}`!".format(', '.join(languages)), embed=self.repo_embed, components=[self.embed_action_row])


def setup(bot):
    "Setup command for the bot"
    bot.add_cog(Finder(bot))
