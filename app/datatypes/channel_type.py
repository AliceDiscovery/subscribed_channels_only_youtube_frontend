""" defines a dataclass that stores a channel's info """
from dataclasses import dataclass


@dataclass(frozen=True)
class ChannelType:
    """ a dataclass that stores a channel's info """
    channel_id: str
    title: str
    handle: str
    subscriber_count: str
    number_of_videos: str
    description: str
    banner_url: str
    profile_pic_url: str
