""" defines a dataclass for representing a video preview (and allowing json serialization) """
from app.datatypes.basetypes import JsonDatatypeABC, constructor_include, json_include


class JsonVideoPreviewElement(JsonDatatypeABC):
    """ defines a dataclass for representing a video preview (and allowing json serialization) """
    def __init__(self,
        channel_id: str,
        banner: str,
        profile_pic: str | None,
        title: str,
        handle: str,
        subscribers: str,
        num_videos: str,
        description: str,
        is_subscribed: bool = False):

        self.validate_setter_type(channel_id, {str}, 'channel_id')
        self.validate_setter_type(banner, {str}, 'banner')
        self.validate_setter_type(profile_pic, {str}, 'profile_pic')
        self.validate_setter_type(title, {str}, 'title')
        self.validate_setter_type(handle, {str}, 'handle')
        self.validate_setter_type(subscribers, {str}, 'subscribers')
        self.validate_setter_type(num_videos, {str}, 'num_videos')
        self.validate_setter_type(description, {str}, 'description')
        self.validate_setter_type(is_subscribed, {bool}, 'is_subscribed')

        self._channel_id = channel_id
        self._banner = banner
        self._profile_pic = profile_pic
        self._title = title
        self._handle = handle
        self._subscribers = subscribers
        self._num_videos = num_videos
        self._description = description
        self._is_subscribed = is_subscribed

    @property
    @json_include
    @constructor_include
    def channel_id(self) -> str:
        return self._channel_id

    @property
    @json_include
    @constructor_include
    def banner(self) -> str:
        return self._banner

    @property
    @json_include
    @constructor_include
    def profile_pic(self) -> str:
        return self._profile_pic

    @property
    @json_include
    @constructor_include
    def title(self) -> str:
        return self._title

    @property
    @json_include
    @constructor_include
    def handle(self) -> str:
        return self._handle

    @property
    @json_include
    @constructor_include
    def subscribers(self) -> str:
        return self._subscribers

    @property
    @json_include
    @constructor_include
    def num_videos(self) -> str:
        return self._num_videos

    @property
    @json_include
    @constructor_include
    def description(self) -> str:
        return self._description

    @property
    @json_include
    @constructor_include
    def is_subscribed(self) -> bool:
        return self._is_subscribed
