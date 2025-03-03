""" implements a function that scrapes the metadata of a YouTube video """

import yt_dlp
from app.datatypes import VideoType
from app.web_scraping_scripts.data_conversion import human_readable_large_numbers, human_readable_times


def scrape_video_data(video_id: str) -> VideoType:
    """ scrapes the metadata of a YouTube video """
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'force_generic_extractor': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)

    return VideoType(
        video_id=video_id,
        title=info_dict.get("title", ""),
        thumbnail=info_dict.get("thumbnail", ""),
        views=human_readable_large_numbers(info_dict.get("view_count", None)),
        description=info_dict.get("description", ""),
        duration=human_readable_times(info_dict.get("duration", None))
    )
