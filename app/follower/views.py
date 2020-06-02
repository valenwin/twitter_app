from flask import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from . import follower_page
from .. import db
from app.user.models import User


@follower_page.route('/<username>', methods=['GET', 'POST'])
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()
    current_user.following.append(user_to_follow)
    db.session.commit()
    return redirect(url_for('user_page.profile'))
