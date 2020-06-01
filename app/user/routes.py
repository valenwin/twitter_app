from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import user_page
from .forms import RegisterForm, LoginForm
from .models import User
from .. import db


@user_page.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('You have been successfully registered.')
        return redirect(url_for('user_page.login'))
    return render_template('user/register.html',
                           form=form)


@user_page.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash('Login failed.')

        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        flash('Login failed.')

    return redirect(url_for('index'))


@login_required
@user_page.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))
