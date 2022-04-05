import os

import aiohttp
from requests.utils import requote_uri

from config import GH_TOKEN
from utils import build_query, logutil
from utils.core import RequestError

logger = logutil.init_logger(os.path.basename(__file__))


""" This will handle all search requests from now on. Provides modularity for future search commands """


async def requester(payload):
    """Our payload structure example:
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
    logger.debug(f"Handling a search request:\n{payload}")
    raw_query = "".join(build_query.build_query(key, payload[key]) for key in payload)

    url = f'https://api.github.com/search/{payload["method"]}?q={requote_uri(raw_query)}&per_page=75'

    logger.debug(f"URL built: {url}")

    try:
        logger.debug("Sending query...")
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=60)
        ) as session:
            async with session.get(
                url,
                headers={"Content-Type": "application/json", "Authorization": GH_TOKEN},
            ) as response:
                return await response.json()
    except Exception as e:
        raise RequestError from e
