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
                process_entries(entry['entries'])
            else:
                if '/shorts/' in entry['url']:
                    shorts.append(ShortType(
                        video_id=entry['id'],
                        title=entry['title'],
                        thumbnail=entry['thumbnails'][-1]['url'],
                        views=human_readable_large_numbers(entry['view_count'])
                    ))
                else:
                    videos.append(VideoType(
                        video_id=entry['id'],
                        title=entry['title'],
                        thumbnail=entry['thumbnails'][-1]['url'],
                        views=human_readable_large_numbers(entry['view_count']),
                        description=entry['description'],
                        duration=human_readable_times(entry['duration'])
                    ))

    process_entries(result['entries'])

    banner_url = None
    profile_pic = None
    for image_url in result['thumbnails']:
        if image_url['id'] == '5':
            banner_url = image_url['url']
        elif image_url['id'] == '7':
            profile_pic = image_url['url']

    channel_info = ChannelType(
        channel_id=channel_id,
        banner=banner_url,
        profile_pic=profile_pic,
        title=result['channel'],
        handle=result['uploader_id'],
        subscribers=human_readable_large_numbers(result['channel_follower_count']),
        num_videos=str(len(videos)+len(shorts)),
        description=result['description']
    )

    return videos, shorts, channel_info
