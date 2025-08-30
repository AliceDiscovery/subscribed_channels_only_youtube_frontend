""" server implementation """
from flask import Flask
from flask_login import LoginManager

from .routes import BLUEPRINTS
from ._server_keys import ServerKey

from .database import init_db, User
from .load_default_themes import init_themes


app = Flask(__name__)
app.config['SECRET_KEY'] = ServerKey().value
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'accounts.login'

init_themes()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


for blueprint in BLUEPRINTS:
    app.register_blueprint(blueprint)


def start_server():
    """ starts the server """
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    start_server()
