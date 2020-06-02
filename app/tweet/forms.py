from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import InputRequired


class TweetForm(FlaskForm):
    text = TextAreaField('Message',
                         validators=[InputRequired('Message is required')])
