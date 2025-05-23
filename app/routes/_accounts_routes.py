""" define all webpage routes relating to user accounts """
from flask import Blueprint, render_template


accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route('/signup')
def signup():
    return render_template('signup.html')


@accounts_bp.route('/login')
def login():
    return render_template('login.html')
