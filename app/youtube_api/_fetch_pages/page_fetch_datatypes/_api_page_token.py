""" implements a dataclass to store data required to fetch another page of api results """
from json import loads, dumps


class ApiPageToken:
    """ a dataclass to store data required to fetch another page of api results """
    def __init__(self, reference=str, token: str|None = None):
        self.reference = reference
        self.token = token

    @property
    def reference(self) -> str:
        """ returns a reference such as a playlist id or a search query for the youtube api """
        return self._reference

    @property
    def token(self) -> str|None:
        """ returns a next page token for the youtube api """
        return self._token

    @token.setter
    def token(self, value: str|None) -> str|None:
        if not isinstance(value, str) and value is not None:
            raise TypeError(f'{self.__class__.__name__}.token must be a str or None, not {type(value)}')
        self._token = value

    def serialize_data(self) -> dict:
        """ returns the data as a dictionary """
        return {
            'reference': self.reference,
            'token': self.token
        }

    def json_serialize(self) -> str:
        """ returns the json representation of the data """
        return dumps(self.serialize_data)

    @classmethod
    def load_json(cls, json: str):
        """ converts a json representation of the class into a class instance """
        data = loads(json)
        return cls(**data)

    def __repr__(self):
        return f'{self.__class__.__name__}(reference={repr(self.reference)}, token={repr(self.token)})'

