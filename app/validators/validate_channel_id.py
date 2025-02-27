""" provides a function to validate channel ids """
import re


def validate_channel_id(channel_id: str) -> bool:
    """ returns true if channel_id is valid (an id may be valid even when the channel doesn't exist) """
    pattern = r'^UC[a-zA-Z0-9\-_]{22}$'
    return bool(re.search(pattern, channel_id))