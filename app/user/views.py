from datetime import datetime

from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.tweet.models import Tweet
from . import user_page
from .forms import RegisterForm, LoginForm
from .models import User
from .. import app, db, config

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@user_page.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            image_filename = f'../../static/images/{photos.save(form.image.data)}'
        except TypeError:
            image_filename = config.Config.DEFAULT_URL_IMG

        user = User(name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    image=image_filename,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        try:
            db.session.commit()
            flash('You have been successfully registered.')
            login_user(user)
            return redirect(url_for('user_page.profile'))
        except IntegrityError:
            db.session.rollback()
            flash('This email is already exist.')
    return render_template('user/register.html',
                           form=form)


@user_page.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            if not user:
                flash('Login failed.')

            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('You have been successfully logged in.')
                return redirect(url_for('user_page.profile'))
            flash('Login failed.')
        except AttributeError:
            pass

    return redirect(url_for('index'))


@user_page.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@user_page.route('/profile', defaults={'username': None})
@user_page.route('/profile/<username>')
@login_required
def profile(username):
    display_follow = True
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
    else:
        user = current_user
    tweets = Tweet.query.filter_by(user=user).all()
    current_time = datetime.now()
    followed_by = user.followed_by.all()
    following = user.following.all()

    if current_user == user:
        display_follow = False
    elif current_user in followed_by:
        display_follow = False

    who_watch = User.query \
        .filter(User.id != user.id) \
        .order_by(db.func.random()) \
        .limit(4).all()

    return render_template('user/profile.html',
                           current_user=user,
                           tweets=tweets,
                           current_time=current_time,
                           followed_by=followed_by,
                           following=following,
                           display_follow=display_follow,
                           who_watch=who_watch)
