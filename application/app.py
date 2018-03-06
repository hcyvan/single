from flask import Flask

from .model import User
from .ext import db, login_manager
from config.config import get_config, get_env


def configure_app(app):
    app.config.from_object(get_config())
    app.config.from_pyfile(get_env())
    return app


def configure_extensions(app):
    db.init_app(app)

    @login_manager.user_loader
    def load_login_user(user_id):
        user = User.query.get(user_id)

        return user


def create_app():
    app = Flask(__name__)
    configure_app(app)
    configure_extensions(app)
    return app
