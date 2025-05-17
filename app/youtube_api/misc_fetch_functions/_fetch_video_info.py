""" implements a function that returns the basic information about a video """

from app.datatypes import VideoType
from app.validators import validate_video_id, ValidationError

from ..api_client import YoutubeDataV3API

from ..youtube_data_convertions import convert_date
from ._fetch_profile_pictures import fetch_profile_picture


def fetch_video_info(api: YoutubeDataV3API, video_id: str) -> VideoType:
    """ returns the basic information about a video """
    if not validate_video_id(video_id):
        raise ValidationError("Invalid video ID")

    request = api.client.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()

    video_data = response.get('items', [{}])[0]

    snippet = video_data.get('snippet', {})
    statistics = video_data.get('statistics', {})

    return VideoType(
        video_id=video_id,
        channel_name=snippet.get('channelTitle', ''),
        channel_id=snippet.get('channelId', ''),
        title=snippet.get('title', ''),
        views=statistics.get('viewCount', ''),
        description=snippet.get('description', ''),
        channel_pic=fetch_profile_picture(api=api, channel_id=snippet.get('channelId', '')),
        date_stamp=convert_date(snippet.get('publishedAt'))
    )
