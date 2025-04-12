""" defines a dataclass for representing a video preview (and allowing json serialization) """
from flask import url_for

from app.datatypes.basetypes import JsonDatatypeABC, constructor_include, json_include


class JsonVideoPreviewElement(JsonDatatypeABC):
    """ defines a dataclass for representing a video preview (and allowing json serialization) """
    def __init__(self,
        uploader_id: str,
        video_id: str,
        thumbnail: str,
        profile_pic: str | None,
        title: str,
        uploader: str,
        view_count: str,
        duration: str,
        description: str,
        is_subscribed: bool = False):

        self.validate_setter_type(uploader_id, {str}, 'uploader_id')
        self.validate_setter_type(uploader_id, {str}, 'video_id')
        self.validate_setter_type(thumbnail, {str}, 'thumbnail')
        self.validate_setter_type(profile_pic, {str}, 'profile_pic')
        self.validate_setter_type(title, {str}, 'title')
        self.validate_setter_type(uploader, {str}, 'uploader')
        self.validate_setter_type(view_count, {str}, 'view_count')
        self.validate_setter_type(duration, {str}, 'duration')
        self.validate_setter_type(description, {str}, 'description')
        self.validate_setter_type(is_subscribed, {bool}, 'is_subscribed')

        self._uploader_id = uploader_id
        self._video_id = video_id
        self._thumbnail = thumbnail
        self._profile_pic = profile_pic
        self._title = title
        self._uploader = uploader
        self._view_count = view_count
        self._duration = duration
        self._description = description
        self._is_subscribed = is_subscribed

    @property
    @json_include
    @constructor_include
    def uploader_id(self) -> str:
        return self._uploader_id
    
    @property
    @json_include
    def uploader_url(self) -> str | None:
        try:
            return url_for('main.channel_overview', channel_id=self.uploader_id)
        except RuntimeError:
            return None

    @property
    @json_include
    @constructor_include
    def video_id(self) -> str:
        return self._video_id

    @property
    @json_include
    def video_url(self) -> str | None:
        try:
            return url_for('main.video_page', video_id=self.video_id)
        except RuntimeError:
            return None

    @property
    @json_include
    @constructor_include
    def thumbnail(self) -> str:
        return self._thumbnail

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
    def uploader(self) -> str:
        return self._uploader

    @property
    @json_include
    @constructor_include
    def view_count(self) -> str:
        return self._view_count

    @property
    @json_include
    @constructor_include
    def duration(self) -> str:
        return self._duration

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
