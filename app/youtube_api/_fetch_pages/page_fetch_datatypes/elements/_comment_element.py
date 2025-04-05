""" defines a dataclass for representing a youtube comment (and allowing json serialization) """
from __future__ import annotations
from typing import List

from flask import url_for

from app.datatypes.basetypes import JsonDatatypeABC, constructor_include, json_include
from app.youtube_api.youtube_data_convertions import human_readable_large_numbers, \
        human_readable_time_delta


class JsonCommentElement(JsonDatatypeABC):
    """ defines a dataclass for representing a youtube comment (and allowing json serialization) """
    def __init__(self,
            comment_id: str,
            text: str,
            like_count: int,
            author: str,
            author_id: str,
            author_thumbnail_url: str,
            is_author_uploader: bool,
            time_stamp: str,
            replies: List[JsonCommentElement] = None):

        self.validate_setter_type(comment_id, {str}, 'comment_id')
        self.validate_setter_type(text, {str}, 'text')
        self.validate_setter_type(like_count, {int}, 'like_count')
        self.validate_setter_type(author, {str}, 'author')
        self.validate_setter_type(author_id, {str}, 'author_id')
        self.validate_setter_type(author_thumbnail_url, {str}, 'author_thumbnail_url')
        self.validate_setter_type(is_author_uploader, {bool}, 'is_author_uploader')
        self.validate_setter_type(time_stamp, {str}, 'time_stamp')

        self._comment_id = comment_id
        self._text = text
        self._like_count = like_count
        self._author = author
        self._author_id = author_id
        self._author_thumbnail_url = author_thumbnail_url
        self._is_author_uploader = is_author_uploader
        self._time_stamp = time_stamp

        self._replies = [] if replies is None else replies
        self.append_reply(*self._replies)

    @property
    @json_include
    @constructor_include
    def comment_id(self) -> str:
        """ returns the youtube id of the comment """
        return self._comment_id

    @property
    @constructor_include
    def text(self) -> str:
        """ returns the text content of the comment """
        return self._text

    @property
    @constructor_include
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
    @constructor_include
    def author(self) -> str:
        """ returns the account name of the comment's author """
        return self._author

    @property
    @constructor_include
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
    @constructor_include
    def author_thumbnail_url(self) -> str:
        """ returns the profile picture url for the comment's author """
        return self._author_thumbnail_url

    @property
    @json_include
    @constructor_include
    def is_author_uploader(self) -> bool:
        """ True if the uploader of the video the comment was posted on is the comment's author """
        return self._is_author_uploader

    @property
    @constructor_include
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
    @constructor_include
    def replies(self) -> List[JsonCommentElement]:
        """ returns the comment's replies as an array """
        return self._replies

    @property
    def reply_count(self) -> int:
        """ returns the raw number of replies """
        return len(self._replies)

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
        self._replies.extend(replies)

    def json_compatible_serialize_data(self) -> dict:
        """ returns the data as a dictionary """
        serial_data = super().json_compatible_serialize_data()

        reply_json = []
        for reply in serial_data.get('replies', []):
            reply_json.append(reply.json_compatible_serialize_data())

        serial_data['replies'] = reply_json
        return serial_data
