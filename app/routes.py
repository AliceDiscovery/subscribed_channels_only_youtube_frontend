""" define all url routes """
from flask import Blueprint, render_template
from app.web_scraping_scripts import scrape_channel_videos


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/channel/<channel_id>')
def channel_overview(channel_id):
    return render_template('channel_overview.html', videos=scrape_channel_videos(channel_id))
