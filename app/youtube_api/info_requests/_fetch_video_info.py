""" implements a function that returns the basic information about a video """
from json import loads

from app.datatypes import VideoType
from app.validators import validate_video_id, ValidationError

from app.youtube_api.subprocesses import FETCH_VIDEO_PREVIEWS, FETCH_PROFILE_PICTURE

from app.youtube_api.youtube_data_convertions import convert_date


def fetch_video_info(video_id: str) -> VideoType:
    """ returns the basic information about a video """
    if not validate_video_id(video_id):
        raise ValidationError("Invalid video ID")

    response = loads(FETCH_VIDEO_PREVIEWS.invoke('--', video_id))

    video_data = response.get('items', [{}])[0]

    snippet = video_data.get('snippet', {})
    statistics = video_data.get('statistics', {})

    profile_picture = ''
    if 'channelId' in snippet.keys():
        profile_picture_dict = loads(FETCH_PROFILE_PICTURE.invoke('--', snippet['channelId']))
        profile_picture = profile_picture_dict.get(snippet['channelId'], '')

    return VideoType(
        video_id=video_id,
        channel_name=snippet.get('channelTitle', ''),
        channel_id=snippet.get('channelId', ''),
        title=snippet.get('title', ''),
        views=statistics.get('viewCount', ''),
        description=snippet.get('description', ''),
        channel_pic=profile_picture,
        date_stamp=convert_date(snippet.get('publishedAt'))
    )
