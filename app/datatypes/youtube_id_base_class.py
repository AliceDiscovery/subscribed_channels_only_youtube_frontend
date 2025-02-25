""" implements abstract base class for YouTube ids (for videos or channel) """
from abc import ABC


class YoutubeIdType(ABC):
    """ abstract base class to represent a YouTube id (for videos or channels) """
    def __init__(self, youtube_id: str):
        self._youtube_id = youtube_id

    @property
    def youtube_id(self):
        """ returns the YouTube id """
        return self._youtube_id
