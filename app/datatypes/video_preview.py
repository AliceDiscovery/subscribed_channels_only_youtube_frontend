""" defines a dataclass that stores metadata about a YouTube video preview """
from .video_base_type import VideoBaseType
from dataclasses import dataclass


@dataclass(frozen=True)
class VideoPreviewType(VideoBaseType):
    """ a dataclass that stores metadata about a YouTube video preview """
    channel_id: str
    channel_name: str
    title: str
    views: str
    thumbnail: str
    description: str
    duration: str
    channel_pic: str
    date_stamp: str
