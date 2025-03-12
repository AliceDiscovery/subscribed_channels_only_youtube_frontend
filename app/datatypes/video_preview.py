""" defines a dataclass that stores metadata about a YouTube video preview """
from .video_base_type import VideoBaseType
from dataclasses import dataclass


@dataclass
class VideoPreviewType(VideoBaseType):
    """ a dataclass that stores metadata about a YouTube video preview """
    title: str
    views: str
    thumbnail: str
    description: str
    duration: str
    date_stamp: str
    channel_id: str = None
    channel_name: str = None
    channel_pic: str = None
