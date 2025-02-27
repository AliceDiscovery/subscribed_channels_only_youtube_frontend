""" defines a dataclass that stores metadata about a YouTube short """
from .video_base_type import VideoBaseType
from dataclasses import dataclass


@dataclass(frozen=True)
class ShortType(VideoBaseType):
    """ a dataclass that stores metadata about a YouTube short """
