""" defines a dataclass that stores metadata about a YouTube long-form video """
from .video_base_type import VideoBaseType
from dataclasses import dataclass


@dataclass(frozen=True)
class VideoType(VideoBaseType):
    """ a dataclass that stores metadata about a YouTube long-form video """
    description: str
    duration: str
