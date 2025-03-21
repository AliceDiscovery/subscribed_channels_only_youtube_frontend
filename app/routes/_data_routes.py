""" define routes for transfering json data """
from flask import Blueprint, jsonify, request
from app.youtube_api import YouTubeAPI


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

