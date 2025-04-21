""" implements a class that stores an instance of the YouTube API client """
from googleapiclient.discovery import build


class YoutubeDataV3API:
    """ a class that stores an instance of the YouTube API client """
    def __init__(self, api_key: str):
        self._client = build('youtube', 'v3', developerKey=api_key)

    @property
    def client(self):
        """ an instance of the YouTube API """
        return self._client
