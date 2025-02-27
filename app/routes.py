""" define all url routes """
from flask import Blueprint, render_template
from app.web_scraping_scripts import scrape_channel_data


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/channel/<channel_id>')
def channel_overview(channel_id):
    videos, shorts, channel_info = scrape_channel_data(channel_id)
    return render_template(
        'channel_overview.html',
        channel_info=channel_info,
        videos=videos,
        shorts=shorts
    )
