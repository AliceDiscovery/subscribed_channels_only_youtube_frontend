""" Implements function that returns YouTube search results """
from yt_dlp import YoutubeDL
from app.datatypes import VideoType, ShortType
from app.web_scraping_scripts import get_several_profile_icons
from app.web_scraping_scripts.data_conversion import human_readable_large_numbers, human_readable_times


def scrape_search_data(query, max_results=50) -> [[VideoType], [ShortType]]:
    """ returns the results of a YouTube search """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)

    # scrape all the profile icon for videos concurrently
    profile_icons = get_several_profile_icons(
        *[entry['channel_id'] for entry in results['entries'] if '/short/' not in entry['url']]
    )

    videos = []
    shorts = []

    for entry in results['entries']:
        if '/shorts/' in entry.get('url', ''):
            shorts.append(ShortType(
                video_id=entry.get('id', ''),
                channel_id=entry.get('channel_id', ''),
                channel_name=entry.get('channel', ''),
                title=entry.get('title', ''),
                thumbnail=entry.get('thumbnails', [{}])[-1].get('url', ''),
                views=human_readable_large_numbers(entry.get('view_count', None))
            ))
        else:
            videos.append(VideoType(
                video_id=entry.get('id', ''),
                channel_id=entry.get('channel_id', ''),
                channel_name=entry.get('channel', ''),
                title=entry.get('title', ''),
                thumbnail=entry.get('thumbnails', [{}])[-1].get('url', ''),
                views=human_readable_large_numbers(entry.get('view_count', None)),
                description=entry.get('description', ''),
                duration=human_readable_times(entry.get('duration', None)),
                channel_pic=profile_icons.get(entry.get('channel_id', ''), '')
            ))

    return videos, shorts
