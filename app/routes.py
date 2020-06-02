from flask import render_template

from app import app
from app.user.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template('base.html', form=form)
