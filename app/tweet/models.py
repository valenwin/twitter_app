from datetime import datetime

from .. import db


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(150), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
