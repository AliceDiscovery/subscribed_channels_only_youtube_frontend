""" implements a datatype to store data required to fetch another page of api results """
from app.datatypes.basetypes import JsonDatatypeABC, constructor_include, json_include


class ApiPageToken(JsonDatatypeABC):
    """ a datatype to store data required to fetch another page of api results """
    def __init__(self,
            video_id: str|None = None,
            channel_id: str|None = None,
            playlist_id: str|None = None,
            search_query: str|None = None,
            token: str|None = None,
            is_last_page: bool = False):

        if not any((video_id, channel_id, playlist_id, search_query)):
            raise ValueError('must provide at least one reference')

        self.validate_argument_type(video_id, {str, None})
        self.validate_argument_type(channel_id, {str, None})
        self.validate_argument_type(playlist_id, {str, None})
        self.validate_argument_type(search_query, {str, None})
        self.validate_argument_type(token, {str, None})
        self.validate_argument_type(is_last_page, {bool})

        self._video_id = video_id
        self._channel_id = channel_id
        self._playlist_id = playlist_id
        self._search_query = search_query
        self._token = token
        self._is_last_page = is_last_page

    @property
    @json_include
    @constructor_include
    def video_id(self) -> str | None:
        """ the target video ID if provided """
        return self._video_id

    @property
    @json_include
    @constructor_include
    def channel_id(self) -> str | None:
        """ the target channel ID if provided """
        return self._channel_id

    @property
    @json_include
    @constructor_include
    def playlist_id(self) -> str | None:
        """ the target playlist ID if provided """
        return self._playlist_id

    @property
    @json_include
    @constructor_include
    def search_query(self) -> str | None:
        """ the search query text if provided """
        return self._search_query

    @property
    @json_include
    @constructor_include
    def token(self) -> str | None:
        """ the token used to fetch the next page """
        return self._token

    @property
    @json_include
    @constructor_include
    def is_last_page(self) -> bool:
        """ boolean value of whether the current page is the last page of content """
        return self._is_last_page
