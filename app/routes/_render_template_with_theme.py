from flask import render_template
from flask_login import current_user

from ..load_default_themes import get_themes as get_default_themes


def render_template_with_theme(*args, **kwargs):
    default_themes_array = get_default_themes()

    if current_user.is_authenticated and current_user.active_default_theme is not None:
        active_user_theme_id = current_user.active_default_theme
        for theme in default_themes_array:
            if theme.get('id') == active_user_theme_id:
                return render_template(*args, **kwargs, theme_variables=theme)

    return render_template(*args, **kwargs)
