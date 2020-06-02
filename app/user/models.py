from datetime import datetime
from functools import partial

from flask_login import UserMixin
from slugify import slugify
from sqlalchemy import Column

from .. import db

NotNullColumn = partial(Column, nullable=False)

followers = db.Table('follower',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followee_id', db.Integer, db.ForeignKey('user.id')))


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
    following = db.relationship('User', secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followee_id == id),
                                backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    followed_by = db.relationship('User', secondary=followers,
                                  primaryjoin=(followers.c.followee_id == id),
                                  secondaryjoin=(followers.c.follower_id == id),
                                  backref=db.backref('followees', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def __init__(self, *args, **kwargs):
        if 'slug' not in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)
