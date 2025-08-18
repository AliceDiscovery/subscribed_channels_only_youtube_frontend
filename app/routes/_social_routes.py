""" define all page routes relating to social aspects of the website """
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, abort
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError
from ..database import db, User, ContentPack, UserContentPack, UserFilter

from ..youtube_api import YouTubeAPI
from ..validators import ValidationError


social_bp = Blueprint('social', __name__)
youtube = YouTubeAPI()


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


@social_bp.route('/edit_filter')
@login_required
def edit_filter_blank():
    return redirect(url_for('user_content_packs'))


@social_bp.route('/edit_filter/<int:packId>', methods=['GET', 'POST'])
@login_required
def edit_filter(packId):
    is_duplicate_id_error = False
    is_invalid_id_error = False

    if request.method == 'POST':
        youtube_id = request.form.get('id', '')
        is_channel_id = request.form.get('is_channel_id') == 'true'
        is_blacklist_filter = request.form.get('is_blacklist_filter') == 'true'

        name = None
        try:
            if is_channel_id:
                name = youtube.fetch_channel_info(youtube_id).title 
            else:
                info = youtube.fetch_video_info(youtube_id)
                name = f'{info.channel_name} - {info.title}'

        except ValidationError:
            is_invalid_id_error = True
        else:
            new_filter = UserFilter(
                user_id=current_user.id,
                content_pack_id=packId,
                name=name,
                is_blacklist_filter=is_blacklist_filter,
                is_channel_id=is_channel_id,
                youtube_id=youtube_id
            )
            try:
                db.session.add(new_filter)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                is_duplicate_id_error = True

    user_filters = UserFilter.query.filter_by(user_id=current_user.id).all()
    return render_template(
        'edit_filter.html',
        pack_id=packId,
        user_filters=user_filters,
        is_duplicate_id_error=is_duplicate_id_error,
        is_invalid_id_error=is_invalid_id_error)


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


@social_bp.route('/delete-list-element/<int:packId>/<int:filter_id>', methods=['POST'])
@login_required
def delete_list_element(packId, filter_id):
    filter_list_element = UserFilter.query.filter_by(
        filter_id=filter_id
    ).first()

    if filter_list_element:
        db.session.delete(filter_list_element)
        db.session.commit()
    
    return redirect(url_for('social.edit_filter', packId=packId))
