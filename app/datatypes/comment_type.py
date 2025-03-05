""" defines a dataclass to represent a viewer comment """
from dataclasses import dataclass


@dataclass
class CommentType:
    """ a dataclass to represent a viewer comment """
    comment_id: str
    text: str
    like_count: str
    has_several_likes: bool
    author_id: str
    author: str
    author_thumbnail_url: str
    author_is_uploader: bool
    author_is_verified: bool
    is_favorited: bool
    is_pinned: bool
    time_str: str
    replies: list
