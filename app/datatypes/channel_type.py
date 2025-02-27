""" defines a dataclass that stores a channel's info """
from dataclasses import dataclass


@dataclass(frozen=True)
class ChannelType:
    """ a dataclass that stores a channel's info """
    channel_id: str
    banner: str
    profile_pic: str
    title: str
    handle: str
    subscribers: str
    num_videos: str
    description: str
    is_subscribed: bool = False
