""" define all webpage routes relating to user accounts """
from flask import Blueprint, request, render_template, jsonify
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..database import db, User
from ..info_convertions import redact_email

accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already in use"}), 400

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return jsonify({"success": "Account created"}), 201

    return render_template('signup.html')


@accounts_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return jsonify({"success": "Login successful"}), 200
        return jsonify({"error": "Invalid email or password"}), 401

    return render_template('login.html')


@accounts_bp.route('/profile')
@login_required
def profile():
    redacted_email = redact_email(current_user.email)
    return render_template('profile.html', redacted_email=redacted_email)


@accounts_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        data = request.json
        cur_password = data.get("curPassword")

        user = User.query.filter_by(email=current_user.email).first()
        if user and check_password_hash(user.password_hash, cur_password):
            new_password = data.get('newPassword')
            hashed_new_password = generate_password_hash(new_password, method="pbkdf2:sha256")
            user.password_hash = hashed_new_password
            db.session.commit()
            return jsonify({"success": "Change successful"}), 200
        return jsonify({"error": "Wrong password"}), 401

    return render_template('change_password.html')


@accounts_bp.route('/change-email')
@login_required
def change_email():
    return render_template('change_email.html')
