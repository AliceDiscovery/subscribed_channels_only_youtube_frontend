""" defines a dataclass that stores metadata about a YouTube long-form video """
from .video_base_type import VideoBaseType
from dataclasses import dataclass, field


@dataclass
class VideoType(VideoBaseType):
    """ a dataclass that stores metadata about a YouTube long-form video """
    channel_id: str
    channel_name: str
    title: str
    views: str
    thumbnail: str = None
    description: str = None
    duration: str = None
    channel_pic: str = None
    date_stamp: str = None
    comments: list = field(default_factory=lambda: [])
