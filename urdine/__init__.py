from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
import pyotp

app = Flask(__name__)

app.config['SECRET_KEY'] = '3f66f25cb0da8a79eb4636dd83a27c4a'  # need this for forms
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///urdine.db"  # need this for database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # shows up when a user tries to access content that requires them to be logged in
login_manager.login_message_category = 'info'  # login message category

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cscclassestest@gmail.com'
app.config['MAIL_PASSWORD'] = 'itsfortesting12345'
mail = Mail(app)


from urdine import routes