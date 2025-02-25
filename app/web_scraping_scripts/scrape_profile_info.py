""" extracts profile data from a channel """
import yt_dlp
from app.datatypes import ChannelType
from app.validators import validate_channel_id, ValidationError
from app.web_scraping_scripts.data_conversion import epoch_to_date


def scrape_profile_info(channel_id: str) -> ChannelType:
    """ extracts profile data from a channel """
    if not validate_channel_id(channel_id):
        raise ValidationError('invalid channel id')

    channel_url = f'https://www.youtube.com/channel/{channel_id}/videos/'

    ydl_opts = {
        'skip_download': True,
        'extract_flat': True,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        channel_info = ydl.extract_info(channel_url, download=False)

    banner_url = None
    profile_pic = None
    for image_url in channel_info['thumbnails']:
        if image_url['id'] == '5':
            banner_url = image_url['url']
        elif image_url['id'] == '7':
            profile_pic = image_url['url']

    return ChannelType(
        channel_id=channel_id,
        title=channel_info['channel'],
        subscriber_count=channel_info['channel_follower_count'],
        description=channel_info['description'],
        banner_url=banner_url,
        profile_pic_url=profile_pic,
        date_created=epoch_to_date(channel_info['epoch'])
    )
