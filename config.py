import os

from dotenv import load_dotenv

load_dotenv()

DEV_GUILD_ID = int(os.environ.get("DEV_GUILD"))

"Enable DEBUG messages for logging"
DEBUG = True

"""The scope for your bot to operate in. This should be a guild ID or list of guild IDs"""
DEV_GUILD = DEV_GUILD_ID
