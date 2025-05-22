""" implements a class for handling high level api requests """
from typing import List

from json import loads

from app.datatypes import VideoType, ChannelType

from .api_key import APIKey
from .api_client import YoutubeDataV3API

from .subprocesses import FETCH_PROFILE_PICTURE

from .get_requests import GetRequestsHandler
from .info_requests import fetch_video_info as _fetch_video_info
from . import misc_fetch_functions as _misc_fetch_functions


class YouTubeAPI:
    """ handles high level api requests """
    def __init__(self):
        self._api = YoutubeDataV3API(api_key=APIKey.VALUE)
        self._get_requests_handler = GetRequestsHandler(self._api)

    @property
    def get_requests(self):
        """ returns handler for handling GET requested api queries """
        return self._get_requests_handler

    @staticmethod
    def fetch_video_info(video_id: str) -> VideoType:
        """ returns info about a video """
        return _fetch_video_info(video_id)

    def fetch_channel_info(self, channel_id: str) -> ChannelType:
        """ returns info about a channel """
        return _misc_fetch_functions.fetch_channel_info(self._api, channel_id)

    @staticmethod
    def fetch_profile_pictures(*channel_ids: [str]) -> List[str]:
        """ retrieves the urls of the profile pictures for multiple channel in parallel """
        profile_picture_dict = loads(FETCH_PROFILE_PICTURE.invoke('--', *channel_ids))
        return [profile_picture_dict.get(channel_id, '') for channel_id in channel_ids]

    @staticmethod
    def fetch_profile_picture(channel_id: str) -> str:
        """ retrieves the url of the profile picture for an individual channel  """
        return loads(FETCH_PROFILE_PICTURE.invoke('--', channel_id)).get(channel_id, '')
