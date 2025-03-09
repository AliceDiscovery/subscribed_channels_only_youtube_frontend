from googleapiclient.discovery import build
from .api_key import APIKey

from app.web_scraping_scripts import get_profile_icon
from app.web_scraping_scripts.data_conversion import convert_date

from app.datatypes import VideoType


class YouTubeAPI:
    def __init__(self):
        self._api = build("youtube", "v3", developerKey=APIKey.VALUE)

    def get_video_page_data(self, video_id: str) -> VideoType:
        request = self._api.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()

        video_data = response.get('items', [])[0]

        snippet = video_data['snippet']
        statistics = video_data['statistics']

        return VideoType(
            video_id=video_id,
            channel_name=snippet['channelTitle'],
            channel_id=snippet['channelId'],
            title=snippet['title'],
            views=statistics['viewCount'],
            description=snippet['description'],
            channel_pic=get_profile_icon(snippet['channelId']),
            date_stamp=convert_date(snippet['publishedAt'])
        )
