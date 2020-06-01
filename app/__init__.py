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
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Blueprints
from .user import user_page
app.register_blueprint(user_page, url_prefix='/user')

from . import routes, models
from .user import routes, models
