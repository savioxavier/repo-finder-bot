# repo-finder-bot

> Find the best repos to contribute to, right from Discord!

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Add to your server

[![Add Repo Finder Bot](https://img.shields.io/badge/-Add%20Repo%20Finder%20Bot-141B2E?style=for-the-badge&logo=discord)](https://discord.com/api/oauth2/authorize?client_id=772682311346159616&permissions=2147871808&scope=bot%20applications.commands)

## FAQs

- **Hmm. What's this?**

This is the Repo Finder Bot, a bot designed to help people find good GitHub repositories to contribute to.

- **How does it work?**

Simple. Whenever you execute the `rf.repo [topic]` command in your server, the bot uses the GitHub API to find a good repository matching the topic and then send an array of details related to it.

- **What sort of details?**

A whole array of details, including basic info ranging from the amount of stars and forks to the latest issues contributed to the repo.

Here's an example:

![Screenshot](https://i.imgur.com/WFXDioS_d.webp?maxwidth=760&fidelity=grand)

- **Why are there no slash commands?**

There was a slight trouble trying to fetch data using slash commands but don't worry, slash commands will be added soon!

- **Why is the code so bad?**

It works.

I'll fix it.

- **Cool bot, can I add it to my server?**

Of course you can! Just click [this link](https://discord.com/api/oauth2/authorize?client_id=772682311346159616&permissions=2147871808&scope=bot%20applications.commands) and select the server of your choice.

- **How can I contribute?**

Just check out the Issues pane for potential issues and submit a PR to solve them. Of course, you can always submit regular PRs not linked to an issue and I'd be happy to accept them!

Icons made by [Freepik](https://www.freepik.com) from [Flaticon](https://www.flaticon.com/).

- **Ok well how can I run it myself?**

> 1. Clone this repo
> 2. Create a Discord bot token [here](https://discord.com/developers)
> 3. Create a personal access token on GitHub [here](https://github.com/settings/tokens) (Make sure to copy it immediately! You "lose" it once you refresh or close the tab)
> 4. Make a new file called `.env` inside the repo folder and paste this code block in the file
> ```
> GH_TOKEN="[paste Github token here]"
> TOKEN="[paste Discord bot token here]"
> ```
> 5. Run `python3 -m pip install -r requirements`. You'll need Python3.6 at least
> 6. After that's done, run the bot at `python3 main.py`
> 
> If you get errors related to missing token environment variables, run `source .env`
