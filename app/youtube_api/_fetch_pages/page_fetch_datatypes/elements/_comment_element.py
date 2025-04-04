""" defines a dataclass for representing a youtube comment (and allowing json serialization) """
from __future__ import annotations
from typing import List
from dataclasses import dataclass, field

from flask import url_for

from app.datatypes.basetypes import JsonDatatypeABC, json_include
from app.youtube_api.youtube_data_convertions import human_readable_large_numbers, \
        human_readable_time_delta


@dataclass
class JsonCommentElement(JsonDatatypeABC):
    """ defines a dataclass for representing a youtube comment (and allowing json serialization) """
    _comment_id: str
    _text: str
    _like_count: int
    _author: str
    _author_id: str
    _author_thumbnail_url: str
    _is_author_uploader: bool
    _time_stamp: str
    _replies: List[JsonCommentElement] = field(default_factory=list)

    def __post_init__(self):
        self.validate_setter_type(self._comment_id, {str}, 'comment_id')
        self.validate_setter_type(self._text, {str}, 'text')
        self.validate_setter_type(self._like_count, {int}, 'like_count')
        self.validate_setter_type(self._author, {str}, 'author')
        self.validate_setter_type(self._author_id, {str}, 'author_id')
        self.validate_setter_type(self._author_thumbnail_url, {str}, 'author_thumbnail_url')
        self.validate_setter_type(self._is_author_uploader, {bool}, 'is_author_uploader')
        self.validate_setter_type(self._time_stamp, {str}, 'time_stamp')

        self._reply_array = []
        self.append_reply(*self._replies)

    @property
    @json_include
    def comment_id(self) -> str:
        """ returns the youtube id of the comment """
        return self._comment_id

    @property
    def text(self) -> str:
        """ returns the text content of the comment """
        return self._text

    @property
    def like_count(self) -> int:
        """ returns the raw number of likes """
        return self._like_count

    @property
    @json_include
    def like_count_formatted(self) -> str:
        """ returns a formatted string of the number of likes """
        number = human_readable_large_numbers(self.like_count)
        unit = 'like' if self._like_count == 1 else 'likes'
        return f'{number} {unit}'

    @property
    @json_include
    def author(self) -> str:
        """ returns the account name of the comment's author """
        return self._author

    @property
    def author_id(self) -> str:
        """ returns the account id of the comment's author """
        return self._author_id

    @property
    @json_include
    def author_url(self) -> str | None:
        """
        returns the internal url for the comment's author's profile page
        or returns None if the flask server isn't active
        """
        try:
            return url_for('main.channel_overview', channel_id=self.author_id)
        except RuntimeError:
            return None

    @property
    @json_include
    def author_thumbnail_url(self) -> str:
        """ returns the profile picture url for the comment's author """
        return self._author_thumbnail_url

    @property
    @json_include
    def is_author_uploader(self) -> bool:
        """ True if the uploader of the video the comment was posted on is the comment's author """
        return self._is_author_uploader

    @property
    def time_stamp(self) -> str:
        """ returns youtube's timestamp of when the comment was posted """
        return self._time_stamp

    @property
    @json_include
    def time_stamp_formatted(self) -> str:
        """ returns a formatted string displaying how long ago the comment was posted """
        return human_readable_time_delta(self.time_stamp)

    @property
    @json_include
    def replies(self) -> List[JsonCommentElement]:
        """ returns the comment's replies as an array """
        return self._reply_array

    @property
    def reply_count(self) -> int:
        """ returns the raw number of replies """
        return len(self._reply_array)

    @property
    @json_include
    def reply_count_formatted(self) -> str:
        """ returns a formatted string of the number of replies """
        number = human_readable_large_numbers(self.reply_count)
        unit = 'reply' if self.reply_count == 1 else 'replies'
        return f'{number} {unit}'

    def append_reply(self, *replies: JsonCommentElement):
        """ adds more replies """
        for reply in replies:
            self.validate_argument_type(reply, {JsonCommentElement})
        self._reply_array.extend(replies)

    def json_compatible_serialize_data(self) -> dict:
        """ returns the data as a dictionary """
        serial_data = super().json_compatible_serialize_data()

        reply_json = []
        for reply in serial_data.get('replies', []):
            reply_json.append(reply.json_compatible_serialize_data())

        serial_data['replies'] = reply_json
        return serial_data
