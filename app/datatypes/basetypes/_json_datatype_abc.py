""" implements a base datatype that can be converted to json """
from json import dumps
from ._datatype_abc import DatatypeABC


class JsonDatatypeABC(DatatypeABC):
    """ implements a base datatype that can be converted to json """
    def json_serialize(self) -> str:
        """ returns the json representation of the data """
        return dumps(self._json_compatible_serialize_data(), indent=4)

    def _json_compatible_serialize_data(self) -> dict:
        return self._serialize_data()
