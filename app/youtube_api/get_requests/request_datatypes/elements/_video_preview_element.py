""" defines a dataclass for representing a video preview (and allowing json serialization) """
from flask import url_for

from app.datatypes.basetypes import JsonDatatypeABC, constructor_include, json_include


class VideoPreviewUploaderInfo(JsonDatatypeABC):
    """ defines a dataclass that store info about a video's upload to be used for video preview """
    def __init__(self, uploader_id: str, uploader: str, profile_picture_url: str):
        self.validate_setter_type(uploader_id, {str}, 'uploader_id')
        self.validate_setter_type(uploader, {str}, 'uploader')
        self.validate_setter_type(profile_picture_url, {str}, 'profile_picture_url')

        self._uploader_id = uploader_id
        self._uploader = uploader
        self._profile_picture_url = profile_picture_url

    @property
    @json_include
    @constructor_include
    def uploader_id(self) -> str:
        """ the ID of the video's uploader """
        return self._uploader_id

    @property
    @json_include
    def uploader_url(self) -> str | None:
        """ the URL of the uploader's page (requires Flask server to be active) """
        try:
            return url_for('main.channel_overview', channel_id=self.uploader_id)
        except RuntimeError:
            return None

    @property
    @json_include
    @constructor_include
    def uploader(self) -> str:
        """ the username of the video's uploader """
        return self._uploader

    @property
    @json_include
    @constructor_include
    def profile_picture_url(self) -> str:
        """ a URL for the uploader's profile picture """
        return self._profile_picture_url


class JsonVideoPreviewElement(JsonDatatypeABC):
    """ defines a dataclass for representing a video preview (and allowing json serialization) """
    def __init__(self,
        uploader_info: VideoPreviewUploaderInfo | None,
        video_id: str,
        thumbnail: str,
        title: str,
        view_count: str,
        duration: str,
        description: str):

        self.validate_setter_type(uploader_info, {VideoPreviewUploaderInfo, None}, 'uploader_info')
        self.validate_setter_type(thumbnail, {str}, 'thumbnail')
        self.validate_setter_type(title, {str}, 'title')
        self.validate_setter_type(view_count, {str}, 'view_count')
        self.validate_setter_type(duration, {str}, 'duration')
        self.validate_setter_type(description, {str}, 'description')

        self._uploader_info = uploader_info
        self._video_id = video_id
        self._thumbnail = thumbnail
        self._title = title
        self._view_count = view_count
        self._duration = duration
        self._description = description

    @property
    @json_include
    @constructor_include
    def uploader_info(self) -> VideoPreviewUploaderInfo | None:
        """ info about the video's uploader (optional) """
        return self._uploader_info

    @property
    @json_include
    def has_uploader_info(self) -> bool:
        """ a boolean value of whether the (optional) uploader's info is available"""
        return bool(self.uploader_info)

    @property
    @json_include
    @constructor_include
    def video_id(self) -> str:
        """ the ID of the video """
        return self._video_id

    @property
    @json_include
    def video_url(self) -> str | None:
        """ the URL to the video's page (requires Flask server to be active) """
        try:
            return url_for('main.video_page', video_id=self.video_id)
        except RuntimeError:
            return None

    @property
    @json_include
    @constructor_include
    def thumbnail(self) -> str:
        """ the URL to the video's thumbnail """
        return self._thumbnail

    @property
    @json_include
    @constructor_include
    def title(self) -> str:
        """ the video's title """
        return self._title

    @property
    @json_include
    @constructor_include
    def view_count(self) -> str:
        """ the video's view count string """
        return self._view_count

    @property
    @json_include
    @constructor_include
    def duration(self) -> str:
        """ the video's duration string """
        return self._duration

    @property
    @json_include
    @constructor_include
    def description(self) -> str:
        """ the video's description """
        return self._description
