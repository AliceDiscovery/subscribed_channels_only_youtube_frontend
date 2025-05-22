from pathlib import Path

from importlib.util import spec_from_file_location, module_from_spec
from sys import modules


def find_parent_path_recursive(target_parent: str, path: Path | str = __file__) -> Path:
    """ recursively truncates a path upto a certain parent directory """
    path = Path(path)
    if path is None or path == path.parent:
        raise NotADirectoryError(f'Parent directory "{target_parent}" not found.')

    if path.name == target_parent:
        return path

    return find_parent_path_recursive(target_parent, path=path.parent)


def import_module_from_path(module_path: Path):
    """ dynamically imports a module from a path """
    module_path = Path(module_path)
    module_name = module_path.stem
    spec = spec_from_file_location(module_name, str(module_path))

    if spec is None:
        raise ModuleNotFoundError(module_path)

    module = module_from_spec(spec)
    modules[module_name] = module
    spec.loader.exec_module(module)

    return module
