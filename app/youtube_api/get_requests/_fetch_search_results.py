""" implements a function that fetches the next page of search results """
from typing import List

from json import loads
from ..subprocesses import FETCH_SEARCH_RESULTS, FETCH_VIDEO_PREVIEWS, FETCH_PROFILE_PICTURE

from .request_datatypes import PageType, ApiPageToken
from .request_datatypes.elements import JsonVideoPreviewElement, VideoPreviewUploaderInfo

from ..youtube_data_convertions import convert_iso_duration, human_readable_large_numbers


def fetch_search_results(page_token: ApiPageToken) -> PageType:
    """ fetches the next page of search results """
    max_results = 50

    def validate_token():
        if page_token.search_query is None:
            raise ValueError('page_token must contain a search_query for this function')

    def fetch_search_response() -> dict:
        """ fetch search results in a separate subprocess """
        args = ['--max-results', str(max_results)]

        if page_token.token is not None:
            args += ['--token', page_token.token]

        args += ['--', page_token.search_query]

        if result := FETCH_SEARCH_RESULTS.invoke(*args):
            return loads(result)
        return {}

    def create_page_token(response) -> ApiPageToken:
        new_token = response.get('nextPageToken')
        return ApiPageToken(
            search_query=page_token.search_query,
            token=new_token,
            is_last_page=(new_token is None)
        )

    def extract_video_ids(response) -> List[str]:
        return [
            video['id']['videoId']
            for video in response.get('items', [])
            if video.get('id', {}).get('videoId')
        ]

    def fetch_profile_pics(video_response) -> List[str | None]:
        channel_ids = [
            video['snippet']['channelId']
            for video in video_response.get('items', [])
            if video.get('snippet', {}).get('channelId')
        ]
        profile_pictures = loads(FETCH_PROFILE_PICTURE.invoke('--', *channel_ids))
        return [profile_pictures.get(channel_id) for channel_id in channel_ids]

    def build_video_previews(video_response, profile_pics) -> List[JsonVideoPreviewElement]:
        previews = []
        for video, profile_pic in zip(video_response.get('items', []), profile_pics):
            video_id = video.get('id')
            if video_id:
                snippet = video.get('snippet', {})
                details = video.get('contentDetails', {})
                stats = video.get('statistics', {})

                preview = JsonVideoPreviewElement(
                    uploader_info=VideoPreviewUploaderInfo(
                        uploader_id=snippet.get('channelId', ''),
                        uploader=snippet.get('channelTitle', ''),
                        profile_picture_url=profile_pic
                    ),
                    video_id=video_id,
                    thumbnail=snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                    title=snippet.get('title', ''),
                    view_count=human_readable_large_numbers(int(stats.get('viewCount', 0))),
                    duration=convert_iso_duration(details.get('duration', '')),
                    description=snippet.get('description', '')
                )
                previews.append(preview)
        return previews

    validate_token()
    search_response = fetch_search_response()
    new_page_token = create_page_token(search_response)
    video_ids = extract_video_ids(search_response)

    if not video_ids:
        return PageType(page=None, page_token=new_page_token)

    video_response = loads(FETCH_VIDEO_PREVIEWS.invoke('--', *video_ids))
    profile_pics_list = fetch_profile_pics(video_response)
    video_previews_list = build_video_previews(video_response, profile_pics_list)
    return PageType(page=video_previews_list, page_token=new_page_token)


def create_search_token(search_query: str) -> ApiPageToken:
    """ creates a blank token used for fetching pages of search results """
    return ApiPageToken(
        search_query=search_query
    )
