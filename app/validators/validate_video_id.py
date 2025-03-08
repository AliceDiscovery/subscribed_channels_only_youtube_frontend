""" provides a function to validate video ids """
import re


def validate_video_id(video_id: str) -> bool:
    """ returns true if video_id is valid (an id may be valid even when the video itself doesn't exist) """
    pattern = r'^[a-zA-Z0-9\-_]{11}$'
    return bool(re.search(pattern, video_id))