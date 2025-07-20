""" define all page routes relating to social aspects of the website """
from flask import Blueprint, render_template
from flask_login import login_required, current_user


social_bp = Blueprint('social', __name__)


@social_bp.route('/content-filters')
@login_required
def user_content_packs():
    content_packs = [
        {
            'content_pack_id': link.content_pack.id,
            'name': link.content_pack.name,
            'is_public': link.content_pack.is_public,
            'is_author': link.content_pack.author_id == current_user.id,
            'is_enabled': link.is_enabled
        }
        for link in current_user.content_pack_links.all()
    ]

    return render_template('content_filters.html', content_packs=content_packs)
