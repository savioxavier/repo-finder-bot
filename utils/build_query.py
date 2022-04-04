import re

from utils import logutil

logger = logutil.init_logger("build_query.py")


def parse_args(content) -> list:
    _whitespace_re = re.compile(r"\s\s+")

    # Formatting rules:
    # if user separates by comma, split and strip spaces
    # if user separates by space, strip duplicate spaces, and replace spaces with commas
    if "," in content:
        content = [s.strip() for s in content.split(",")]
    elif " " in content:  # noqa
        content = _whitespace_re.sub(" ", content)
        content = content.split(" ")
    else:
        content = [content]

    return content


def build_query(key, value):
    logger.debug(f"Building a query with key:\n{key} : {value}")

    raw_query = ""

    if key in ["topics", "languages"]:
        if len(value) > 1:
            for i in value:
                if len(raw_query) > 0 and raw_query[-1] != "+":
                    # Prevent malformed queries by appending a "+" at the end if there is none
                    raw_query += "+"

                # Just remove the last letter, topics -> topic
                raw_query += f"{key[:-1]}:{str(i)}+"
        else:
            if len(raw_query) > 0 and raw_query[-1] != "+":
                # Prevent malformed queries by appending a "+" at the end if there is none
                raw_query += "+"

            raw_query += f"{key[:-1]}:{value[0]}+"
    elif key == "issue":
        if value:
            raw_query += ("is:issue+" if value["type"] == "issue" else "is:pr+") + (
                "is:open+" if value["isOpen"] is True else ""
            )
    elif key == "searchQuery":
        if value:
            raw_query += f'"{value}"' if value else ""

    return raw_query
