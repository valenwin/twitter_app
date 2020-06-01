from flask import Blueprint

from app import login_manager
from app.user.models import User

user_page = Blueprint('user_page', __name__)

from app.user import routes


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))
