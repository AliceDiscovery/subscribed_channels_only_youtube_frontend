""" implements a base datatype that can be converted to json """
from typing import Callable, TypeVar

from json import dumps
from ._datatype_abc import DatatypeABC


F = TypeVar('F', bound=Callable)

def json_include(func: F) -> F:
    """ defines a decorator that addes a property to the json output """
    return func


class JsonDatatypeABC(DatatypeABC):
    """ implements a base datatype that can be converted to json """
    def json_serialize(self) -> str:
        """ returns the json representation of the data """
        return dumps(self.json_compatible_serialize_data(), indent=4)

    def json_compatible_serialize_data(self) -> dict:
        return self.serialize_data(json_include)
