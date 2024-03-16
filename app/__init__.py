from flask import Flask
from flask_cors import CORS
from app.views import auth_blueprint
from flask_bcrypt import Bcrypt


def create_app():
    app = Flask(__name__)

    CORS(app)

    bcrypt = Bcrypt(app)

    app.register_blueprint(auth_blueprint)

    return app
