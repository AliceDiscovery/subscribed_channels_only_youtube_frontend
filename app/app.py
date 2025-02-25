""" server implementation """
from flask import Flask
from .routes import bp


app = Flask(__name__)
app.register_blueprint(bp)


def start_server():
    """ starts the server """
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    start_server()
