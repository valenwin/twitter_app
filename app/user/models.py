from datetime import datetime
from functools import partial

from flask_login import UserMixin
from slugify import slugify
from sqlalchemy import Column

from .. import db

NotNullColumn = partial(Column, nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    username = NotNullColumn(db.String(250), unique=True)
    email = NotNullColumn(db.String, unique=True)
    password = NotNullColumn(db.String)
    image = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.now)
    slug = db.Column(db.String(), nullable=True)
    tweets = db.relationship('Tweet', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def __init__(self, *args, **kwargs):
        if 'slug' not in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)
