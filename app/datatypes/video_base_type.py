""" defines a base dataclass that store metadata about a YouTube video """
from dataclasses import dataclass


@dataclass(frozen=True)
class VideoBaseType:
    """ a base dataclass that store metadata about a YouTube video """
    video_id: str
    title: str
    thumbnail: str
    views: str
