from flask import render_template

from app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')


@app.route('/profile', methods=['GET', 'POST'])
def index2():
    return render_template('profile.html')


@app.route('/register', methods=['GET', 'POST'])
def index3():
    return render_template('register.html')


@app.route('/timeline', methods=['GET', 'POST'])
def index4():
    return render_template('timeline.html')
