""" defines a dataclass that stores metadata about a YouTube short """
from .video_base_type import VideoBaseType
from dataclasses import dataclass


@dataclass(frozen=True)
class ShortType(VideoBaseType):
    """ a dataclass that stores metadata about a YouTube short """
    channel_id: str
    channel_name: str
    title: str
    views: str
    thumbnail: str = None
    description: str = None
    duration: str = None
    channel_pic: str = None
    date_stamp: str = None
