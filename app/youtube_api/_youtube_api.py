from googleapiclient.discovery import build
from .api_key import APIKey

from app.web_scraping_scripts import get_profile_icon, get_several_profile_icons
from app.web_scraping_scripts.data_conversion import convert_date, human_readable_large_numbers

from app.datatypes import VideoType, VideoPreviewType


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

    def get_search_results(self, query: str, max_results=10) -> [VideoPreviewType]:
        """ searches YouTube and returns results as a list of video previews """

        search_request = self._api.search().list(
            part='snippet',
            q=query,
            maxResults=max_results,
            type='video'  # restrict results to videos for now
        )
        search_response = search_request.execute()

        video_ids = [
            video['id']['videoId']
            for video in search_response.get('items', [])
            if video.get('id', {}).get('videoId')
        ]
        if not video_ids:
            return []

        video_request = self._api.videos().list(
            part='snippet,contentDetails,statistics',
            id=','.join(video_ids)
        )
        video_response = video_request.execute()

        channel_icons = get_several_profile_icons(
            *[video['snippet']['channelId']
                for video in video_response.get('items', [])
                if video.get('snippet', {}).get('channelId')
            ]
        )

        video_previews = []
        for video in video_response.get('items', []):
            video_id = video.get('id')
            if video_id:
                video_snippet = video.get('snippet', {})
                video_content_details = video.get('contentDetails', {})
                video_statistics = video.get('statistics', {})

                video = VideoPreviewType(
                    video_id=video_id,
                    channel_id=video_snippet.get('channelId', ''),
                    channel_name=video_snippet.get('channelTitle', ''),
                    title=video_snippet.get('title', ''),
                    views=human_readable_large_numbers(int(video_statistics.get('viewCount', 0))),
                    thumbnail=video_snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                    description=video_snippet.get('description', ''),
                    duration=video_content_details.get('duration', ''),  # this is returned in a different format
                    channel_pic=channel_icons.get(video_snippet.get('channelId'), ''),
                    date_stamp=convert_date(video_snippet.get('publishedAt'))
                )
                video_previews.append(video)

        return video_previews
