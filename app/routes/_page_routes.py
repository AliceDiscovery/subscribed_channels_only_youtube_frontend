""" define all wepage_bpage routes """
from flask import Blueprint, render_template
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
def search_results(search_terms):
    videos = youtube.get_search_results(search_terms)
    return render_template(
        'search_results_page.html',
        videos=videos,
        shorts=[]  # shorts have not been tested yet
    )


@page_bp.route('/channel/<channel_id>')
def channel_overview(channel_id):
    channel_info, videos, next_page_token = youtube.get_channel_page(channel_id)
    return render_template(
        'channel_overview.html',
        channel_info=channel_info,
        videos=videos,
        next_page_token=next_page_token,
        shorts=[]  # sorting of shorts not implemented yet
    )


@page_bp.route('/video/<video_id>')
def video_page(video_id):
    video_data = youtube.get_video_page(video_id)
    return render_template(
        'video_page.html',
        video=video_data,
        comments=video_data.comments
    )

