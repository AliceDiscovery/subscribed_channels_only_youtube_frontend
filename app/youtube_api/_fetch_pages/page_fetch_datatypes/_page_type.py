""" implements json-serializable page of content for GET requests """
from app.datatypes.basetypes import JsonDatatypeABC, constructor_include, json_include
from ._api_page_token import ApiPageToken


class PageType(JsonDatatypeABC):
    """ json-serializable page of content for GET requests """
    def __init__(self, page: JsonDatatypeABC, page_token: ApiPageToken):
        self.validate_argument_type(page_token, {ApiPageToken})

        self._page = page
        self._page_token = page_token

    @property
    @json_include
    @constructor_include
    def page(self):
        """ returns the content """
        return self._page

    @property
    @json_include
    @constructor_include
    def page_token(self) -> str:
        """ returns the token datatype that is needed to fetch the next page """
        return self._page_token
