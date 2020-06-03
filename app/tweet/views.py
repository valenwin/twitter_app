from datetime import datetime

from flask import flash, abort
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app.user.models import User
from app.user.models import followers
from . import tweet_page
from .forms import TweetForm
from .models import Tweet
from .. import db, app


@app.template_filter('time_since')
def time_since(delta):
    seconds = delta.total_seconds()

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days > 0:
        return '%dd' % days
    elif hours > 0:
        return '%dh' % hours
    elif minutes > 0:
        return '%dm' % minutes
    else:
        return 'Just now'


@tweet_page.route('/')
def tweets():
    tweets_all = Tweet.query.all()
    current_time = datetime.now()
    return render_template('tweet/tweets.html',
                           tweets=tweets_all,
                           current_time=current_time)


@tweet_page.route('/timeline', defaults={'username': None})
@tweet_page.route('/timeline/<username>')
@login_required
def timeline(username):
    form = TweetForm()

    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
        tweets = Tweet.query.filter_by(user=user) \
            .order_by(Tweet.created.desc()).all()
    else:
        user = current_user
        tweets = Tweet.query.join(followers, (followers.c.followee_id == Tweet.user_id)) \
            .filter(followers.c.follower_id == current_user.id) \
            .order_by(Tweet.created.desc()).all()

    current_time = datetime.now()

    who_watch = User.query \
        .filter(User.id != user.id) \
        .order_by(db.func.random()) \
        .limit(4).all()

    followed_by = user.followed_by.all()

    return render_template('tweet/timeline.html',
                           form=form,
                           tweets=tweets,
                           current_time=current_time,
                           current_user=user,
                           who_watch=who_watch,
                           followed_by=followed_by)


@tweet_page.route('/post_tweet', methods=['POST'])
@login_required
def post_tweet():
    form = TweetForm()
    if form.validate():
        tweet = Tweet(
            user_id=current_user.id,
            text=form.text.data
        )
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for('tweet_page.timeline'))
    return flash('Something went wrong.')
