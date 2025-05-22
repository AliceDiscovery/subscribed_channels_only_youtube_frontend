""" implements a handler for api requests triggered by GET requests """
from ..api_client import YoutubeDataV3API
from .request_datatypes import ApiPageToken, PageType

from . import _fetch_channel_videos
from . import _fetch_search_results
from . import _fetch_video_comments


class GetRequestsHandler:
    """ handles high level api requests that support GET requests for fetching more data """
    def __init__(self, api: YoutubeDataV3API):
        self._api = api

    @staticmethod
    def fetch_channel_videos(channel_id: str) -> PageType:
        """ fetches the first page of videos uploaded to a specific channel """
        token = _fetch_channel_videos.create_channel_token(channel_id=channel_id)
        return _fetch_channel_videos.fetch_channel_videos(token)

    @staticmethod
    def fetch_search_results(search_query: str) -> PageType:
        """ fetches the first page of search results """
        token = _fetch_search_results.create_search_token(search_query=search_query)
        return _fetch_search_results.fetch_search_results(token)

    @staticmethod
    def fetch_video_comments(video_id: str) -> PageType:
        """ fetches the first page of comments under a video """
        token = _fetch_video_comments.create_comments_token(video_id=video_id)
        return _fetch_video_comments.fetch_video_comments(token)

    @staticmethod
    def fetch_more_channel_videos(token: ApiPageToken) -> PageType:
        """ fetches subsequent pages of videos uploaded to a channel """
        return _fetch_channel_videos.fetch_channel_videos(token)

    @staticmethod
    def fetch_more_search_results(token: ApiPageToken) -> PageType:
        """ fetches subsequent pages of search results """
        return _fetch_search_results.fetch_search_results(token)

    @staticmethod
    def fetch_more_video_comments(token: ApiPageToken) -> PageType:
        """ fetches subsequent pages of comments under a video """
        return _fetch_video_comments.fetch_video_comments(token)
