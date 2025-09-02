import os
import json


THEMES_DIR = "default_themes/"
FALLBACK_THEMES = [
    {'name': 'fallback', 'id': 'fallback-1', 'background-color': '#ffffff', 'foreground-color': '#000000', 'warning-color': '#ff0000'}
]


__default_themes = []  # run `init_themes()`


def validate_theme(theme: dict) -> None:
    required_keys = {'name', 'id', 'background-color', 'foreground-color', 'warning-color'}

    def check_for_missing_keys() -> None:
        if not required_keys.issubset(theme.keys()):
            missing_keys = required_keys - set(theme.keys())
            raise ValueError(f'Theme is missing the following keys: {missing_keys}')
    
    def check_for_additional_keys() -> None:
        extra_keys = set(theme.keys()) - required_keys
        if extra_keys:
            raise ValueError(f'Theme contains additional keys which are not allowed: {extra_keys}')
    
    def validate_value_type() -> None:
        for key, value in theme.items():
            if not isinstance(value, str):
                raise ValueError(f"The value for key '{key}' is not a string. It is of type {type(value).__name__}. Please add quotation marks around the value.")
    
    def validate_non_numeric_id() -> None:
        try:
            int(theme['id'])
        except ValueError:
            pass
        else:
            raise ValueError(f'The theme id must NOT be a number.')
    
    def validate_id_length() -> None:
        if len(theme['id']) > 16:
            raise ValueError(f"The theme id is too long; maximum size is 16 characters. Current length: {theme['id']}")
    
    check_for_missing_keys()
    check_for_additional_keys()
    validate_value_type()
    validate_non_numeric_id()


def _load_theme(theme_path: str) -> dict:
    with open(theme_path, 'r') as f:
        try:
            theme_data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ValueError(f'Invalid JSON in file {theme_path}: {e}')

        else:
            if not isinstance(theme_data, dict):
                raise ValueError(f'Invalid JSON in file {theme_path}; theme must be formatted as a dictionary.')
            try:
                validate_theme(theme_data)
            except ValueError as e:
                raise ValueError(f'Invalid JSON in file {theme_path}: {e}')
        return theme_data


def _load_theme_directory(themes_dir) -> list[dict]:
    themes = []
    seen = {}
    
    for filename in os.listdir(themes_dir):
        if not filename.endswith('.json'):
            continue
        
        theme_path = os.path.join(themes_dir, filename)
        try:
            theme = _load_theme(theme_path)
            theme_id = theme['id']
            
            if theme_id in seen:
                first_name = seen[theme_id]
                raise ValueError(
                    f'Failed to load {filename}; Duplicate theme id "{theme_id}" with loaded theme "{first_name}".'
                )
            
            seen[theme_id] = filename
            themes.append(theme)
        
        except ValueError as e:
            print(e)
    
    return themes


def init_themes() -> None:
    global __default_themes

    themes = _load_theme_directory(THEMES_DIR)
    if not themes:
        print('ERROR: unable to load default themes; loading with fallback themes.')
        themes = FALLBACK_THEMES

    themes.sort(key=lambda x: x['id'])
    __default_themes = themes


def get_themes() -> [dict]:
    return __default_themes


for theme in FALLBACK_THEMES:
    validate_theme(theme)


if __name__ == "__main__":
    init_themes()
    print(get_themes())
