""" define routes for transferring json data """
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from json import loads

from app.youtube_api import YouTubeAPI
from app.youtube_api.get_requests.request_datatypes import ApiPageToken

from ..database import db, Subscription


data_bp = Blueprint('data', __name__, url_prefix='/data')
youtube = YouTubeAPI()


@data_bp.route('/get-channel-videos', methods=['GET'])
def get_channel_videos():
    page_token_dict = loads(request.headers.get('token', {}))
    page_token = ApiPageToken(**page_token_dict)

    return_data = youtube.get_requests.fetch_more_channel_videos(
        token=page_token
    )

    return jsonify({'data': return_data.json_compatible_serialize_data()})


@data_bp.route('/get-search-results', methods=['GET'])
def get_search_results():
    page_token_dict = loads(request.headers.get('token', {}))
    page_token = ApiPageToken(**page_token_dict)

    return_data = youtube.get_requests.fetch_more_search_results(
        token=page_token
    )

    return jsonify({'data': return_data.json_compatible_serialize_data()})


@data_bp.route('/get-comments', methods=['GET'])
def get_comments():
    page_token_dict = loads(request.headers.get('token', {}))
    page_token = ApiPageToken(**page_token_dict)

    return_data = youtube.get_requests.fetch_more_video_comments(
        token=page_token
    )

    return jsonify({'data': return_data.json_compatible_serialize_data()})


@data_bp.route('/channel/<channel_id>', methods=['GET', 'POST'])
@login_required
def is_subscribed(channel_id):
    sub = (
        Subscription
        .query
        .filter_by(user_id=current_user.id, channel_id=channel_id)
        .first()
    )

    if request.method == 'GET':
        if not sub:
            return {'subscribed': False}
        return {
            'subscribed': True,
            'created_at': sub.created_at.isoformat()
        }

    elif request.method == 'POST':
        data = request.get_json()
        new_status = data.get('subscribed')

        if new_status:
            if not sub:
                new_subscription = Subscription(user_id=current_user.id, channel_id=channel_id)
                db.session.add(new_subscription)
                db.session.commit()
                return {'subscribed': True}
            else:
                return {'subscribed': True}
        else:
            if sub:
                db.session.delete(sub)
                db.session.commit()
            return {'subscribed': False}
