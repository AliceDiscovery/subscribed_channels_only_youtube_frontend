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

    active_theme = db.relationship(
        'Theme',
        foreign_keys=[active_theme_id],
        lazy='joined'
    )

    themes = db.relationship(
        'Theme',
        foreign_keys='Theme.user_id',
        back_populates='owner',
        lazy='dynamic'
    )

    def __init__(self, *args, **kwargs):
        """ Assign a default theme to each new User."""
        super().__init__(*args, **kwargs)

        if self.active_theme_id is None:
            default = Theme.query.filter_by(is_default=True).first()
            if default:
                self.active_theme = default


class Theme(db.Model):
    __tablename__ = 'themes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(32), nullable=False)
    is_default = db.Column(db.Boolean, default=False)

    background_color = db.Column(db.String(20), nullable=False)
    foreground_color = db.Column(db.String(20), nullable=False)
    warning_color = db.Column(db.String(20), nullable=False)

    owner = db.relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='themes'
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
    def add_default_themes():
        if Theme.query.count() == 0:
            default_themes = [
                Theme(name='light', background_color="#ffffff", foreground_color="#000000", warning_color="#ff0000", is_default=True),
                Theme(name='dark', background_color="#000000", foreground_color="#ffffff", warning_color="#ffff00", is_default=True)
            ]
            db.session.bulk_save_objects(default_themes)
            db.session.commit()

    db.init_app(app)
    with app.app_context():
        db.create_all()
        add_default_themes()
