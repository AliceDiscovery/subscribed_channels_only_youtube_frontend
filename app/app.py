""" server implementation """
from flask import Flask

from .routes import BLUEPRINTS
from ._server_keys import ServerKey

from .database import db, init_db


app = Flask(__name__)
app.config['SECRET_KEY'] = ServerKey.value
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

init_db(app)


for blueprint in BLUEPRINTS:
    app.register_blueprint(blueprint)


def start_server():
    """ starts the server """
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    start_server()
