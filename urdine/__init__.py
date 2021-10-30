from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '3f66f25cb0da8a79eb4636dd83a27c4a'  # need this for forms
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"  # need this for database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from urdine import routes