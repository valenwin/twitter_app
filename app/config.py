from pathlib import Path
from environs import Env

basedir = Path(Path(__file__).parent).resolve()
env = Env()
env.read_env()


class Config(object):
    UPLOADED_PHOTOS_DEST = 'images'
    DEFAULT_URL_IMG = 'http://127.0.0.1:5000/_uploads/photos/default-user-image.png'
    SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = env.str("SECRET_KEY")
    SITE_URL = "localhost:5000"
    SECURITY_PASSWORD_SALT = env.str("SECURITY_PASSWORD_SALT")
