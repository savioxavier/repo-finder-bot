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

You can also search for multiple topics, eg: `rf.repo [topic1] [topic2]`.

You can even search repos of specific languages *and* topics using the `rf.repolang [languages] [topics]` command.

- **What sort of details?**

A whole array of details, including basic info ranging from the amount of stars and forks to the latest issues contributed to the repo.

Here's an example:

![Screenshot](https://i.imgur.com/WFXDioS_d.webp?maxwidth=760&fidelity=grand)

- **Why are there no slash commands?**

There was a slight trouble trying to fetch data using slash commands but don't worry, slash commands will be added soon!

- **Cool bot, can I add it to my server?**

Of course you can! Just click [this link](https://discord.com/api/oauth2/authorize?client_id=772682311346159616&permissions=2147871808&scope=bot%20applications.commands) and select the server of your choice.

- **Why is the code so bad?**

Because we need you! A number of contributors are helping to expand and improve the code base. Why don't you join us?

- **How can I contribute?**

Just check out the Issues pane for potential issues and submit a PR to solve them. Of course, you can always submit regular PRs not linked to an issue and I'd be happy to accept them!

Please read CONTRIBUTING.md for more information on contributing and building a development environment.


- **How do I run the bot myself?**

> 1. Clone this repository
> 2. Create a Discord bot token from [here](https://discord.com/developers/applications/)
> 3. Create a GitHub personal access token from [here](https://github.com/settings/tokens/) (Make sure to copy it immediately! You "lose" it once you refresh or close the tab)
> 4. Make a new file called `.env` inside the repo folder and paste the below code block in the file
> ```
> GH_TOKEN="[paste Github token here]"
> TOKEN="[paste Discord bot token here]"
> DEV_GUILD=[paste your bot testing server ID here]
> ```
> 5. Run `pip install -r requirements.txt` to install packages. You'll require Python 3.6 or better
> 6. Once that's done, run the bot by executing `python3 main.py` in the terminal
>
> If you aren't sure how to obtain your server ID, check out [this article](https://www.alphr.com/discord-find-server-id/)
> 
> If you get errors related to missing token environment variables, run `source .env`


- **How do I run this bot via Docker?**

> 1. Clone this repository
> 2. Create a Discord bot token from [here](https://discord.com/developers/applications/)
> 3. Create a GitHub personal access token from [here](https://github.com/settings/tokens/) (Make sure to copy it immediately! You "lose" it once you refresh or close the tab)
> 4. Make a new file called `.env` inside the repo folder and paste the below code block in the file
> ```
> GH_TOKEN="[paste Github token here]"
> TOKEN="[paste Discord bot token here]"
> DEV_GUILD=[paste your bot testing server ID here]
> ```
> 5. Run `docker build -t repo-finder-bot .` (don't forget the period at the end)
> 6. Run `docker container run --rm repo-finder-bot`
>
> If you aren't sure how to obtain your server ID, check out [this article](https://www.alphr.com/discord-find-server-id/)


## Contributors

Thanks to all the contributors, without whom this project would not have been possible.

<a href="https://github.com/savioxavier/repo-finder-bot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=savioxavier/repo-finder-bot" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

Icons made by [Freepik](https://www.freepik.com) from [Flaticon](https://www.flaticon.com/).
