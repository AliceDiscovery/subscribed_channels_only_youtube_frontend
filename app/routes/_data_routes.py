""" define routes for transferring json data """
from flask import Blueprint, jsonify, request
from json import loads

from app.youtube_api import YouTubeAPI

from app.youtube_api._fetch_pages.page_fetch_datatypes import ApiPageToken


data_bp = Blueprint('data', __name__, url_prefix='/data')
youtube = YouTubeAPI()


@data_bp.route('/get-channel-videos', methods=['GET'])
def get_channel_videos():
    playlist_id = request.headers.get('playlist-id')
    next_page_token = request.headers.get('next-page-token')

    if next_page_token == 'null':
        next_page_token = None

    video_page, next_page_token = youtube.get_page_of_videos_from_channel(
        playlist_id=playlist_id,
        next_page_token=next_page_token
    )

    return jsonify({'page': video_page, 'next-page-token': next_page_token})


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
    video_id = request.headers.get('video-id')
    channel_id = request.headers.get('channel-id')
    next_page_token = request.headers.get('next-page-token')

    if channel_id == 'null':
        channel_id = None

    if next_page_token == 'null':
        next_page_token = None

    comments, next_page_token = youtube.get_video_comments(
        video_id=video_id,
        channel_id=channel_id,
        next_page_token=next_page_token
    )

    return jsonify({'page': comments, 'next-page-token': next_page_token})

