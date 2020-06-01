from flask import render_template

from app import app
from app.user.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template('base.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def index2():
    return render_template('profile.html')


@app.route('/timeline', methods=['GET', 'POST'])
def index4():
    return render_template('timeline.html')
