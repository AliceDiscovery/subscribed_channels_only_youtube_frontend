""" server implementation """
from flask import Flask
from .routes import BLUEPRINTS


app = Flask(__name__)

for blueprint in BLUEPRINTS:
    app.register_blueprint(blueprint)


def start_server():
    """ starts the server """
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    start_server()

