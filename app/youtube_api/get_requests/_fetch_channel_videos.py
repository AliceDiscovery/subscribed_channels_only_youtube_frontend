""" implements a function that fetches the next page of videos uploaded to a specific channel """
from typing import List
from .._api_client import YoutubeDataV3API

from .request_datatypes import PageType, ApiPageToken
from .request_datatypes.elements import JsonVideoPreviewElement
from ..youtube_data_convertions import human_readable_large_numbers, convert_iso_duration


def fetch_channel_videos(api: YoutubeDataV3API, token: ApiPageToken) -> PageType:
    """ fetches the next page of videos uploaded to a specific channel """
    def get_playlist_id(channel_id: str):
        response = api.client.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()
        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    def build_video_previews(video_response) -> List[JsonVideoPreviewElement]:
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
                    description=snippet.get('description', ''),
                    is_subscribed=False  # subscription tracking not implemented yet
                )
                previews.append(preview)
        return previews

    playlist_id = token.playlist_id
    if playlist_id is None:
        if token.channel_id is None:
            raise ValueError('token must contain a channel_id for this function')
        playlist_id = get_playlist_id(token.channel_id)

    video_id_response = api.client.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50,
        pageToken=token.token
    ).execute()

    new_token = video_id_response.get('nextPageToken')
    new_page_token = ApiPageToken(
        playlist_id=playlist_id,
        is_last_page=(new_token is None),
        token=new_token
    )

    video_ids = [video_id
                 for video in video_id_response.get('items', {})
                 if (video_id := video.get('snippet', {}).get('resourceId').get('videoId', ''))
                 ]

    # if there are no videos uploaded to the channel
    if not video_ids:
        return PageType(page=[], page_token=new_page_token)

    video_response = api.client.videos().list(
        part='snippet,contentDetails,statistics',
        id=','.join(video_ids)
    ).execute()

    preview_array = build_video_previews(video_response)

    return PageType(page=preview_array, page_token=new_page_token)


def create_channel_token(channel_id: str) -> ApiPageToken:
    """ creates a blank token used for fetching pages of videos from a channel """
    return ApiPageToken(
        channel_id=channel_id
    )
