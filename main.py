from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def home():
    render_template('index.html')


@app.route('/register')
def register():
    pass


@app.route('/login')
def login():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5000)