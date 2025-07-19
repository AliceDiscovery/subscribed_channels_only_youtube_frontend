""" implements a function that fetches the next page of videos uploaded to a specific channel """
from typing import List

from json import loads
from ..subprocesses import FETCH_CHANNEL_VIDEOS, FETCH_CHANNEL_PLAYLIST_ID, FETCH_VIDEO_PREVIEWS

from .request_datatypes import PageType, ApiPageToken
from .request_datatypes.elements import JsonVideoPreviewElement
from ..youtube_data_convertions import human_readable_large_numbers, convert_iso_duration


def fetch_channel_videos(page_token: ApiPageToken) -> PageType:
    """ fetches the next page of videos uploaded to a specific channel """
    max_results = 50

    def run_fetch_channel_videos() -> dict:
        """ fetch channel videos in a separate subprocess """
        args = ['--max-results', str(max_results)]

        if page_token.token is not None:
            args += ['--token', page_token.token]

        args += ['--', playlist_id]

        if result := FETCH_CHANNEL_VIDEOS.invoke(*args):
            return loads(result)
        return {}

    def build_video_previews(*video_ids: str) -> List[JsonVideoPreviewElement]:
        video_response = FETCH_VIDEO_PREVIEWS.invoke('--', *video_ids)
        video_response = loads(video_response)

        previews = []
        for video in video_response.get('items', []):
            video_id = video.get('id')
            if video_id:
                snippet = video.get('snippet', {})
                details = video.get('contentDetails', {})
                stats = video.get('statistics', {})

                preview = JsonVideoPreviewElement(
                    uploader_info=None,
                    video_id=video_id,
                    thumbnail=snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                    title=snippet.get('title', ''),
                    view_count=human_readable_large_numbers(int(stats.get('viewCount', 0))),
                    duration=convert_iso_duration(details.get('duration', '')),
                    description=snippet.get('description', '')
                )
                previews.append(preview)
        return previews

    playlist_id = page_token.playlist_id
    if playlist_id is None:
        if page_token.channel_id is None:
            raise ValueError('token must contain a channel_id for this function')
        playlist_id = FETCH_CHANNEL_PLAYLIST_ID.invoke('--', page_token.channel_id)

    channel_videos_response = run_fetch_channel_videos()
    new_token = channel_videos_response.get('nextPageToken')
    new_page_token = ApiPageToken(
        playlist_id=playlist_id,
        is_last_page=(new_token is None),
        token=new_token
    )

    video_ids = [video_id
                 for video in channel_videos_response.get('items', {})
                 if (video_id := video.get('snippet', {}).get('resourceId', {}).get('videoId', ''))
                 ]

    # if there are no videos uploaded to the channel
    if not video_ids:
        return PageType(page=[], page_token=new_page_token)

    preview_array = build_video_previews(*video_ids)

    return PageType(page=preview_array, page_token=new_page_token)


def create_channel_token(channel_id: str) -> ApiPageToken:
    """ creates a blank token used for fetching pages of videos from a channel """
    return ApiPageToken(
        channel_id=channel_id
    )
