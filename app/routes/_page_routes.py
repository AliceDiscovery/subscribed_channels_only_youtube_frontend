""" define all webpage routes """
from flask import Blueprint, render_template
from flask_login import login_required
from app.youtube_api import YouTubeAPI


page_bp = Blueprint('main', __name__)
youtube = YouTubeAPI()


@page_bp.route('/')
def index():
    return render_template('index.html')


@page_bp.route('/search/')
def search():
    return render_template('search_page.html')


@page_bp.route('/search/<search_terms>')
@login_required
def search_results(search_terms):
    search_results_first_page = youtube.get_requests.fetch_search_results(search_terms)
    return render_template(
        'search_results_page.html',
        search_results_first_page=search_results_first_page.json_serialize()
    )


@page_bp.route('/channel/<channel_id>')
@login_required
def channel_overview(channel_id):
    channel_info = youtube.fetch_channel_info(channel_id)
    channel_videos_first_page = youtube.get_requests.fetch_channel_videos(channel_id)
    return render_template(
        'channel_overview.html',
        channel_info=channel_info,
        channel_videos_first_page=channel_videos_first_page.json_serialize()
    )


@page_bp.route('/video/<video_id>')
@login_required
def video_page(video_id):
    video_data = youtube.fetch_video_info(video_id)
    video_comments_first_page = youtube.get_requests.fetch_video_comments(video_id)
    return render_template(
        'video_page.html',
        video=video_data,
        video_comments_first_page=video_comments_first_page.json_serialize()
    )
