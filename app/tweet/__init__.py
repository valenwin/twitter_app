from flask import Blueprint

from app import login_manager
from app.user.models import User

tweet_page = Blueprint('tweet_page', __name__)

from app.tweet import views


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))
