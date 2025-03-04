""" define all url routes """
from flask import Blueprint, render_template
from app.web_scraping_scripts import scrape_channel_data, scrape_search_data, scrape_video_data


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/search/<search_terms>')
def search(search_terms):
    videos, shorts = scrape_search_data(search_terms)
    return render_template(
        'search_page.html',
        videos=videos,
        shorts=shorts
    )


@bp.route('/channel/<channel_id>')
def channel_overview(channel_id):
    videos, shorts, channel_info = scrape_channel_data(channel_id)
    return render_template(
        'channel_overview.html',
        channel_info=channel_info,
        videos=videos,
        shorts=shorts
    )

@bp.route('/video/<video_id>')
def video_page(video_id):
    video_data = scrape_video_data(video_id)
    return render_template(
        'video_page.html',
        video=video_data
    )
