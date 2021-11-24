from flask import render_template, request, Blueprint
from urdine.models import Post
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html', currYear = datetime.now().year)

@main.route('/about')
def about():
    return render_template('about.html', title='About')