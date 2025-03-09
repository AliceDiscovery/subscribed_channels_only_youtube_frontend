""" defines a base dataclass that store metadata about a YouTube video """
from dataclasses import dataclass


@dataclass(frozen=True)
class VideoBaseType:
    """ a base dataclass that store metadata about a YouTube video """
    video_id: str
    channel_id: str
    channel_name: str
    title: str
    views: str
    thumbnail: str = None
