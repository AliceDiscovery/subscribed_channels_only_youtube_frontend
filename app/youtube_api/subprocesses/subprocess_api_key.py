""" allows the APIKey class to be accessed from within a subprocess """
import importlib.util
import os


# the module to be imported from the parent directory
module_name = 'api_key'


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
module_path = os.path.join(parent_dir, f'{module_name}.py')

spec = importlib.util.spec_from_file_location(module_name, module_path)
api_key = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_key)


# casts name
APIKey = api_key.APIKey
