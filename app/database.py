from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    subscriptions = db.relationship(
        'Subscription',
        backref='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    content_pack_links = db.relationship(
        'UserContentPack',
        back_populates='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
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


class ContentPack(db.Model):
    __tablename__ = 'content_packs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=False)

    author = db.relationship('User', backref='content_packs', lazy='joined')

    user_links = db.relationship(
        'UserContentPack',
        back_populates='content_pack',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )


class UserContentPack(db.Model):
    __tablename__ = 'user_content_packs'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    content_pack_id = db.Column(db.Integer, db.ForeignKey('content_packs.id'), primary_key=True)
    is_enabled = db.Column(db.Boolean, default=True, nullable=False)

    user = db.relationship('User', back_populates='content_pack_links')
    content_pack = db.relationship('ContentPack', back_populates='user_links')


class UserFilter(db.Model):
    __tablename__ = 'user_filters'

    filter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_pack_id = db.Column(db.Integer, db.ForeignKey('content_packs.id'), nullable=False)
    is_blacklist_filter = db.Column(db.Boolean, nullable=False)
    is_channel_id = db.Column(db.Boolean, nullable=False)
    youtube_id = db.Column(db.String(24), unique=True, nullable=False)


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
