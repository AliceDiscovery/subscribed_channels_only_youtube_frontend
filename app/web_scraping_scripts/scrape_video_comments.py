""" implements a function that scrapes all the comments of a YouTube video """
import yt_dlp
from app.validators import validate_video_id, ValidationError
from app.web_scraping_scripts.data_conversion import human_readable_large_numbers
from app.datatypes import CommentType


def scrape_video_comments(video_id: str):
    """ scrapes all the comments of a YouTube video """
    if not validate_video_id(video_id):
        raise ValidationError('invalid channel id')

    video_url = f'https://www.youtube.com/watch?v={video_id}'

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'getcomments': True,
        'force_generic_extractor': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(video_url, download=False)

    comments = {}
    for raw_comment in results.get('comments'):
        comment = CommentType(
            comment_id=raw_comment.get('id', ''),
            text=raw_comment.get('text', ''),
            like_count=human_readable_large_numbers(raw_comment.get('like_count')),
            author_id=raw_comment.get('author_id', ''),
            author=raw_comment.get('author', ''),
            author_thumbnail_url=raw_comment.get('author_thumbnail', ''),
            author_is_uploader=raw_comment.get('author_is_uploader', False),
            author_is_verified=raw_comment.get('author_id_verified', False),
            is_favorited=raw_comment.get('is_favorited', False),
            is_pinned=raw_comment.get('is_pinned', False),
            time_str=raw_comment.get('_time_text', ''),
            replies=[]
        )

        if raw_comment.get('parent') == 'root':
            comments[comment.comment_id] = comment
        else:
            try:
                comments[raw_comment.get('parent')].replies.append(comment)
            except KeyError:
                pass
    return comments.values()
