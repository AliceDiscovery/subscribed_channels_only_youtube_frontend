""" implements a function that fetches the next page of videos uploaded to a specific channel """
from typing import List

from pathlib import Path
from subprocess import check_output
from json import loads

from sys import executable as python_path

from ..api_client import YoutubeDataV3API
from .request_datatypes import PageType, ApiPageToken
from .request_datatypes.elements import JsonVideoPreviewElement
from ..youtube_data_convertions import human_readable_large_numbers, convert_iso_duration


def fetch_channel_videos(api: YoutubeDataV3API, page_token: ApiPageToken) -> PageType:
    """ fetches the next page of videos uploaded to a specific channel """
    max_results = 50

    def run_fetch_channel_videos() -> dict:
        """ fetch channel videos in a separate subprocess """
        target_file = 'fetch_channel_videos_cli.py'
        directory = Path(__file__).parent.parent / 'subprocesses'
        full_target_path = directory / target_file

        command = [
                python_path, full_target_path,
                playlist_id,
                '--max-results', str(max_results)]

        if page_token.token is not None:
            command += ['--token', page_token.token]

        try:
            result = check_output(command)
            return loads(result)
        except KeyboardInterrupt:
            raise
        except Exception as error:
            print(f'Error in {target_file} subprocess: {error}')
            return {}

    def fetch_playlist_id(channel_id: str) -> str | None:
        target_file = 'get_playlist_id.py'
        directory = Path(__file__).parent.parent / 'subprocesses'
        full_target_path = directory / target_file

        command = [
                python_path, full_target_path,
                channel_id
        ]

        try:
            return check_output(command).decode('utf-8').strip()
        except Exception as error:
            print(f'Error in {target_file} subprocess: {error}')
            return None

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

    playlist_id = page_token.playlist_id
    if playlist_id is None:
        if page_token.channel_id is None:
            raise ValueError('token must contain a channel_id for this function')
        playlist_id = fetch_playlist_id(page_token.channel_id)

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
