from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app import config

app = Flask(__name__)
Bootstrap(app)

app.config.from_object(config.Config)

login_manager = LoginManager(app)
login_manager.login_view = 'user_page.login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Blueprints
from .user import user_page
from .tweet import tweet_page
from .follower import follower_page

# Register Blueprints
app.register_blueprint(user_page, url_prefix='/user')
app.register_blueprint(tweet_page, url_prefix='/tweet')
app.register_blueprint(follower_page, url_prefix='/follow')

from . import routes, models
from .user import views, models
from .tweet import views, models
from .follower import views, models