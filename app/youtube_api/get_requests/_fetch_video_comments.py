""" fetches YouTube comments on a video """
from typing import List
from ..api_client import YoutubeDataV3API

from pathlib import Path
from subprocess import check_output
from json import loads

from sys import executable as python_path

from .request_datatypes import PageType, ApiPageToken
from .request_datatypes.elements import JsonCommentElement


def fetch_video_comments(api: YoutubeDataV3API, page_token: ApiPageToken) -> PageType:
    """ fetches YouTube comments on a video """
    max_results = 100

    def convert_comments(comment_response: dict, video_uploader_id: str) -> List[JsonCommentElement]:
        def convert_single_comment(snippet: dict, comment_id: str) -> JsonCommentElement:
            author_channel_id = snippet['authorChannelId']['value']
            return JsonCommentElement(
                comment_id=comment_id,
                text=snippet['textDisplay'],
                like_count=snippet['likeCount'],
                author=snippet['authorDisplayName'],
                author_id=author_channel_id,
                author_thumbnail_url=snippet['authorProfileImageUrl'],
                is_author_uploader=(author_channel_id == video_uploader_id),
                time_stamp=snippet['publishedAt']
            )

        comment_array = []
        try:
            for root_comment in comment_response['items']:
                comment_element = convert_single_comment(
                    snippet=root_comment['snippet']['topLevelComment']['snippet'],
                    comment_id=root_comment['id']
                )

                if 'replies' in root_comment:
                    for reply_comment in root_comment['replies']['comments']:
                        reply = convert_single_comment(
                            snippet=reply_comment['snippet'],
                            comment_id=reply_comment['id']
                        )
                        comment_element.append_reply(reply)

                comment_array.append(comment_element)
        except KeyError as error:
            new_error_msg = f'YouTube has changed their json for Comments; {error} not found'
            raise KeyError(new_error_msg) from error
        return comment_array


    def fetch_video_comments() -> dict:
        """ fetch video comments in a seperate subprocess """
        target_file = 'fetch_video_comments_cli.py'
        directory = Path(__file__).parent.parent / 'subprocesses'
        full_target_path = directory / target_file

        command = [
                python_path, full_target_path,
                page_token.video_id,
                '--max-results', str(max_results)]

        if page_token.token is not None:
            command += ['--token', page_token.token]

        try:
            result = check_output(command)
            return loads(result)
        except Exception as error:
            print(f'Error in {target_file} subprocess: {error}')
            return {}

    def get_channel_id(video_id: str) -> str:
        video_response = api.client.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        if not video_response.get('items'):
            raise ValueError('Invalid video ID or video not found')

        try:
            return video_response.get('items', [{}])[0].get('snippet', {})['channelId']
        except KeyError as error:
            new_error_msg = f'YouTube has changed their json for Comments; {error} not found'
            raise KeyError(new_error_msg) from error

    if page_token.video_id is None:
        raise ValueError('page_token must contain a video_id for this function')

    # channel_id is needed to check if a comment's author is the video's uploader
    channel_id = page_token.channel_id
    if channel_id is None:
        channel_id = get_channel_id(page_token.video_id)

    # fetch a page of comments
    comment_response = fetch_video_comments()
    comments = convert_comments(comment_response, channel_id)

    # create token for fetching next page
    new_token = comment_response.get('nextPageToken')
    new_page_token = ApiPageToken(
        video_id=page_token.video_id,
        channel_id=channel_id,
        token=new_token,
        is_last_page=(new_token is None)

    )
    return PageType(page=comments, page_token=new_page_token)


def create_comments_token(video_id: str) -> ApiPageToken:
    """ creates a blank token used for fetching pages of comments under a video """
    return ApiPageToken(
        video_id=video_id
    )
