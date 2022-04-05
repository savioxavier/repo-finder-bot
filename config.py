from dotenv import load_dotenv

from env_handler import load_var, validate_env

load_dotenv()

validate_env()

TOKEN = load_var("TOKEN")
GH_TOKEN = load_var("GH_TOKEN")
DEV_GUILD_ID = load_var("DEV_GUILD")

# Enable DEBUG messages for logging
DEBUG = False

# The scope for your bot to operate in. This should be a guild ID or list of guild IDs
# Due to interactions.py conventions, this should be an int, so we will have to cast it to int type
DEV_GUILD = int(DEV_GUILD_ID)
