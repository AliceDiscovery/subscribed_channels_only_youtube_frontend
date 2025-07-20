""" define all page routes relating to social aspects of the website """
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from ..database import db, User, ContentPack, UserContentPack


social_bp = Blueprint('social', __name__)


@social_bp.route('/content-filters', methods=['GET', 'POST'])
@login_required
def user_content_packs():
    def create_content_pack(user_id: int, pack_name: str, is_public: bool = False, is_enabled: bool = True):
        """ create a content pack and set it's state """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f'User with ID {user_id} does not exist.')

        new_pack = ContentPack(
            name=pack_name,
            author_id=user_id,
            is_public=is_public
        )
        db.session.add(new_pack)
        db.session.flush()

        link = UserContentPack(
            user_id=user_id,
            content_pack_id=new_pack.id,
            is_enabled=is_enabled
        )
        db.session.add(link)
        db.session.commit()

    if request.method == 'POST':
        create_content_pack(current_user.id, pack_name='demo pack')
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
