""" allows the APIKey class to be accessed from within a subprocess """
from ._import_from_parent import find_parent_path_recursive, import_module_from_path


_DIRECTORY = 'youtube_api'
_FILENAME = 'api_key.py'

_module = import_module_from_path(find_parent_path_recursive(_DIRECTORY) / _FILENAME)

APIKey = _module.APIKey
__all__ = ['APIKey']
