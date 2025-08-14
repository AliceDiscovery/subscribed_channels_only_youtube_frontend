""" define all page routes relating to social aspects of the website """
from flask import Blueprint, render_template, request, jsonify
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
        pack_name = request.form['filterNameInput']
        create_content_pack(current_user.id, pack_name=pack_name)
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


@social_bp.route('/toggle-content-pack/<int:packId>', methods=['POST'])
@login_required
def toggle_content_pack(packId):
    user_content_pack = UserContentPack.query.filter_by(
        content_pack_id=packId, user_id=current_user.id
    ).first()

    if not user_content_pack:
        return jsonify(success=False, error="Content pack not found for this user"), 404

    user_content_pack.is_enabled = not user_content_pack.is_enabled
    db.session.commit()
    return jsonify(success=True), 200
