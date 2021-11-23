import os
import secrets
import pyotp
from PIL import Image
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort,jsonify, make_response
from urdine.forms import RegistrationForm, LoginForm, UpdateForm, PostForm, RequestResetForm, ResetPasswordForm
from urdine import app, db, bcrypt, mail
from urdine.models import User, Post, Hall, Station, Food
from flask_login import login_required, login_user, current_user, logout_user
from flask_mail import Message


@app.route('/')
def home():
    return render_template('index.html', currYear = datetime.now().year)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

# REGISTRATION LOGIC

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}! You are now able to log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

# LOGIN LOGIC
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get(
                'next')  # to redirect to the page the user wanted to access before being asked to login
            # return login_2fa(next_page=next_page)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f"Login Unsuccessful! Check username and password", 'danger')
    return render_template('login.html', form=form, title='Login')


def save_picture(pic):
    random_hex = secrets.token_hex(8)
    _, ext_name = os.path.splitext(pic.filename)
    picture_name = random_hex + ext_name
    pic_path = os.path.join(app.root_path, 'static/images', picture_name)
    output_size = (200, 200)
    i = Image.open(pic)
    i.thumbnail(output_size)
    i.save(pic_path)
    return picture_name


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            if current_user.image_file != 'default.jpg':
                os.remove(os.path.join(app.root_path, 'static/images', current_user.image_file))
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated!', 'success')
        redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'images/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)


# LOGOUT LOGIC

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# PASSWORD RESET LOGIC

def send_reset_email(user:User):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''
To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}

If you did not make this request, then ignore this email and no changes will be made.
    '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent with instructions to reset password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<string:token>", methods=['GET', 'POST'])
def reset_password(token:str):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash("Your password has been updated. You can now login!", "success")
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route('/dininghall/<int:hall_id>')
def go_to_hall(hall_id:int):
    hall = Hall.query.get_or_404(hall_id)
    print(hall.name, hall.station)
    return render_template('dining_hall.html', hall_name=hall.name, stations = hall.station)


@app.route('/dininghall/reviews/<int:food_id>', methods=['GET', 'POST'])
@login_required
def review_food(food_id):
    form = PostForm()
    food = Food.query.filter_by(id=food_id).first()
    print(food)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(food=str(food.id)).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    # raise RuntimeError
    print(posts)
    if form.validate_on_submit():
        post = Post(content=form.content.data, food=food_id, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Review added", "success")
        return redirect(url_for('review_food', food_id=food.id))
    return render_template('review.html', form=form, food=food, posts = posts)


@app.route('/review/<post_id>/delete', methods=['POST'])
@login_required
def delete_review(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your review has been deleted', 'success')
    return redirect(url_for('review_food', food_id=int(post.food)))


############# API 

@app.route('/reviews/<hall_name>/<station_name>/<food_name>', methods=['GET'])
def get_reviews(hall_name, station_name, food_name):
    hall = Hall.query.filter_by(name=hall_name).first()
    station = Station.query.filter_by(hall_id=hall.id).first()
    foods = Food.query.filter_by(station_id=station.id).all()
    map = {f'{food.name}': food.post for food in foods}
    reviews = [f"{review.author.username} ({review.date_posted.strftime('%Y-%m-%d')}) - {review.content}" for review in map[food_name]]
    return jsonify({food_name: reviews})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/reviews/1', methods=['POST'])
def test():
    return jsonify({'review': 1})

@app.route('/review/<hall_name>/<station_name>/<food_name>', methods=['POST'])
def create_review(hall_name, station_name, food_name):
    print('x')
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        abort(400)
    review_content = {
        'username': request.json['username'],
        'password': request.json['password'],
        'content': request.json['content'],
    }
    
    user = User.query.filter_by(username=review_content['username']).first()
    if user and bcrypt.check_password_hash(user.password, review_content['password']):
        # raise RuntimeError
        food = Food.query.filter_by(name=food_name).first()
        review = Post(content=review_content['content'], food=str(food.id), user_id=user.id)
        db.session.add(review)
        db.session.commit()
    else:
        return jsonify({'error': 'User not in database'})

    return jsonify({'review': review.content}), 201
