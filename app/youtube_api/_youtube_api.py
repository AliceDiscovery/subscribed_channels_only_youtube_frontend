from typing import List
from app.datatypes import VideoType, ChannelType

from .api_key import APIKey
from ._api_client import YoutubeDataV3API

from .get_requests import GetRequestsHandler
from . import misc_fetch_functions as _misc_fetch_functions


class YouTubeAPI:
    def __init__(self):
        self._api = YoutubeDataV3API(api_key=APIKey.VALUE)
        self._get_requests_handler = GetRequestsHandler(self._api)

    @property
    def get_requests(self):
        return self._get_requests_handler

    def fetch_video_info(self, video_id: str) -> VideoType:
        return _misc_fetch_functions.fetch_video_info(self._api, video_id)

    def fetch_channel_info(self, channel_id: str) -> ChannelType:
        return _misc_fetch_functions.fetch_channel_info(self._api, channel_id)

    def fetch_profile_pictures(self, *channel_ids: [str]) -> List[str]:
        return _misc_fetch_functions.fetch_profile_pictures(self._api, *channel_ids)

    def fetch_profile_picture(self, channel_id: str) -> str:
        return _misc_fetch_functions.fetch_profile_picture(self._api, channel_id)
