from urdine import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    image_file = db.Column(
        db.String(250), nullable=False, default='default.jpg')
    password = db.Column(db.String(40), nullable=False)
    posts = db.relationship('Post', backref='author',
                            lazy=True)  # backref is related to the User. It creates a ghost attribute in the Post relation

    # a User posts Post | you can do user.posts to get the posts of the user
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    food = db.Column(db.String(30),  db.ForeignKey('food.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # you can do post.author to get info of the author

    def __repr__(self):
        return f"Post('{self.date_posted}')"


class Hall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    station = db.relationship('Station', backref='station',
                              lazy=True)

    def __repr__(self) -> str:
        return f"Hall('{self.id}'','{self.name}')"

# grab and go, pit, and connections in order


class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey('hall.id'), nullable=False)
    food = db.relationship('Food', backref='item',
                           lazy=True)

    def __repr__(self) -> str:
        return f"Station('{self.name}')"


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    image_file = db.Column(db.Text, nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey(
        'station.id'), nullable=False)
    post = db.relationship('Post', backref='review',
                           lazy=True)

    def __repr__(self) -> str:
        return f"Food('{self.name}')"


# db.session.add(instance_of_relation_goes_here)
# db.session.commit() commits to the database
# relation_name.query.all() gives you a list | relation_name.query.first() gives you first relation_name.query |
# relation_name.query.filter_by(condition).first()
