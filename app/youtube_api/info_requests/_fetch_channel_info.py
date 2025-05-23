""" implements a function that returns the basic information about a channel """
from json import loads

from app.datatypes import ChannelType
from app.validators import validate_channel_id, ValidationError

from app.youtube_api.subprocesses import FETCH_CHANNEL_INFO


def fetch_channel_info(channel_id: str) -> ChannelType:
    """ returns the basic information about a channel """
    if not validate_channel_id(channel_id):
        raise ValidationError('Invalid channel ID')

    channel_response = loads(FETCH_CHANNEL_INFO.invoke('--', channel_id))

    if not channel_response.get('items', []):
        raise ValidationError('Channel not found')

    channel_data = channel_response.get('items', [])[0]
    channel_snippet = channel_data.get('snippet', {})
    channel_statistics = channel_data.get('statistics', {})
    channel_content_details = channel_data.get('contentDetails', {})
    channel_branding = channel_data.get('brandingSettings', {})
    channel_info = ChannelType(
        channel_id=channel_id,
        banner=channel_branding.get('image', {}).get('bannerExternalUrl', ''),
        profile_pic=channel_snippet.get('thumbnails', {}).get('default', {}).get('url', None),
        title=channel_snippet.get('title', ''),
        handle=channel_snippet.get('customUrl', ''),
        subscribers=channel_statistics.get('subscriberCount', 0),
        num_videos=channel_statistics.get('videoCount', 0),
        playlist_id=channel_content_details.get('relatedPlaylists', {}).get('uploads', []),
        description=channel_snippet.get('description', '')
    )
    return channel_info
