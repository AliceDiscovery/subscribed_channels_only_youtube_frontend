import yt_dlp
from app.datatypes import VideoType, ShortType, ChannelType
from app.web_scraping_scripts.data_conversion import human_readable_large_numbers, human_readable_times
from app.validators import validate_channel_id, ValidationError


def scrape_channel_data(channel_id: str) -> [[VideoType], [ShortType], ChannelType]:
    if not validate_channel_id(channel_id):
        raise ValidationError('invalid channel id')

    channel_url = f'https://www.youtube.com/channel/{channel_id}'

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(channel_url, download=False)

    videos = []
    shorts = []

    def process_entries(entries):
        for entry in entries:
            if 'entries' in entry:  # if channel has both a videos tab and a shorts tab
                process_entries(entry.get('entries', ''))
            else:
                if '/shorts/' in entry.get('url', ''):
                    shorts.append(ShortType(
                        video_id=entry.get('id', ''),
                        channel_id=channel_id,
                        channel_name=result.get('channel', ''),
                        title=entry.get('title', ''),
                        thumbnail=entry.get('thumbnails', [{}])[-1].get('url', ''),
                        views=human_readable_large_numbers(entry.get('view_count', None))
                    ))
                else:
                    videos.append(VideoType(
                        video_id=entry.get('id', ''),
                        channel_id=channel_id,
                        channel_name=result.get('channel', ''),
                        title=entry.get('title', ''),
                        thumbnail=entry.get('thumbnails', [{}])[-1].get('url', ''),
                        views=human_readable_large_numbers(entry.get('view_count', None)),
                        description=entry.get('description', ''),
                        duration=human_readable_times(entry.get('duration', None))
                    ))

    process_entries(result['entries'])

    banner_url = None
    profile_pic = None
    for image_url in result.get('thumbnails', []):
        if image_url.get('id', '') == '5':
            banner_url = image_url.get('url', '')
        elif image_url.get('id', '') == '7':
            profile_pic = image_url.get('url', '')

    channel_info = ChannelType(
        channel_id=channel_id,
        banner=banner_url,
        profile_pic=profile_pic,
        title=result.get('channel', ''),
        handle=result.get('uploader_id', ''),
        subscribers=human_readable_large_numbers(result.get('channel_follower_count', None)),
        num_videos=str(len(videos) + len(shorts)),
        description=result.get('description', '')
    )

    return videos, shorts, channel_info
