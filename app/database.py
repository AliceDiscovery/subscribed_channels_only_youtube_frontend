from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    active_theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=True)

    subscriptions = db.relationship(
        'Subscription',
        backref='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )


class Theme(db.Model):
    __tablename__ = 'themes'

    id = db.Column(db.Integer, primary_key=True)
    background_color = db.Column(db.String(20), nullable=False)
    foreground_color = db.Column(db.String(20), nullable=False)
    warning_color = db.Column(db.String(20), nullable=False)


class UserTheme(db.Model):
    __tablename__ = 'user_themes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'theme_id', name='uix_user_theme'),
    )

User.themes = db.relationship(
    'Theme',
    secondary='user_themes',
    backref=db.backref('users', lazy='dynamic'),
    lazy='dynamic'
)



class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel_id = db.Column(db.String(100), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'channel_id', name='uix_user_channel'),
    )


def is_subscribed(user_id: str, channel_id: str):
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f'User with ID {user_id} does not exist.')

    sub = (
        Subscription
        .query
        .filter_by(user_id=user_id, channel_id=channel_id)
        .first()
    )

    return bool(sub)


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
