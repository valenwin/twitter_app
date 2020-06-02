from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

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
                    email=form.email.data,
                    image=image_filename,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        try:
            db.session.commit()
            flash('You have been successfully registered.')
            return redirect(url_for('index'))
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
                return redirect(url_for('index'))
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


@user_page.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html',
                           current_user=current_user)
