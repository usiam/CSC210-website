from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, jsonify, make_response)
from flask_login import current_user, login_required
from urdine import db
from urdine.models import Hall, Post, Food, Station
from urdine.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/dininghall/<int:hall_id>')
def go_to_hall(hall_id:int):
    hall = Hall.query.get_or_404(hall_id)
    print(hall.name, hall.station)
    return render_template('dining_hall.html', hall_name=hall.name, stations = hall.station)


@posts.route('/dininghall/reviews/<int:food_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.review_food', food_id=food.id))
    return render_template('review.html', form=form, food=food, posts = posts)


@posts.route('/review/<post_id>/delete', methods=['POST'])
@login_required
def delete_review(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your review has been deleted', 'success')
    return redirect(url_for('posts.review_food', food_id=int(post.food)))


@posts.route('/reviews/<hall_name>/<station_name>/<food_name>', methods=['GET'])
def get_reviews(hall_name, station_name, food_name):
    hall = Hall.query.filter_by(name=hall_name).first()
    station = Station.query.filter_by(hall_id=hall.id).first()
    foods = Food.query.filter_by(station_id=station.id).all()
    map = {f'{food.name}': food.post for food in foods}
    reviews = [f"{review.author.username} ({review.date_posted.strftime('%Y-%m-%d')}) - {review.content}" for review in map[food_name]]
    return jsonify({food_name: reviews})


@posts.route('/review/<hall_name>/<station_name>/<food_name>', methods=['POST'])
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


@posts.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)