from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from urdine.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# shows up when a user tries to access content that requires them to be logged in
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'  # login message category
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    from urdine.users.routes import users
    from urdine.posts.routes import posts
    from urdine.main.routes import main
    from urdine.errors.handlers import errors
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app
