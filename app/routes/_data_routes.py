""" define routes for transferring json data """
from flask import Blueprint, jsonify, request
from json import loads

from app.youtube_api import YouTubeAPI

from app.youtube_api.get_requests.request_datatypes import ApiPageToken


data_bp = Blueprint('data', __name__, url_prefix='/data')
youtube = YouTubeAPI()


@data_bp.route('/get-channel-videos', methods=['GET'])
def get_channel_videos():
    page_token_dict = loads(request.headers.get('token', {}))
    page_token = ApiPageToken(**page_token_dict)

    return_data = youtube.fetch_channel_videos(
        token=page_token
    )

    return jsonify({'data': return_data.json_compatible_serialize_data()})


@data_bp.route('/get-search-results', methods=['GET'])
def get_search_results():
    page_token_dict = loads(request.headers.get('token', {}))
    page_token = ApiPageToken(**page_token_dict)

    return_data = youtube.fetch_search_results(
        token=page_token
    )

    return jsonify({'data': return_data.json_compatible_serialize_data()})


@data_bp.route('/get-comments', methods=['GET'])
def get_comments():
    page_token_dict = loads(request.headers.get('token', {}))
    page_token = ApiPageToken(**page_token_dict)

    return_data = youtube.fetch_video_comments(
        token=page_token
    )

    return jsonify({'data': return_data.json_compatible_serialize_data()})
