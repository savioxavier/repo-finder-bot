import logging

# @staticmethod
def build_query(key, value):
    logging.debug(f"Building a query with key:\n{key} : {value}")
    raw_query = ""
    if key in ["topics", "languages"]:
        if len(value) > 1:
            for i in value:
                if len(raw_query) > 0 and raw_query[-1] != "+":
                    # Prevent malformed queries by appending a "+" at the end if there is none
                    raw_query += "+"
                # Just remove the last letter, topics -> topic
                raw_query += key[:len(key) - 1] + ":" + str(i) + "+"
        else:
            if len(raw_query) > 0 and raw_query[-1] != "+":
                # Prevent malformed queries by appending a "+" at the end if there is none
                raw_query += "+"
            raw_query += key[:len(key) - 1] + ":" + value[0] + "+"
    elif key == "issue":
        if value:
            raw_query += ("is:issue+" if value["type"] == "issue" else "is:pr+"
                            ) + ("is:open+" if value["isOpen"] is True else "")
    elif key == "searchQuery":
        if value:
            raw_query += "\"{}\"".format(value) if value else ""
    return raw_query